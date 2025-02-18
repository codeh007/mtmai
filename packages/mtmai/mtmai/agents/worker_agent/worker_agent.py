import asyncio
import os
import sys
from typing import Any, Mapping, Sequence, cast

from agents.teams_agent import TeamBuilderAgent
from autogen_agentchat.base import TaskResult, Team
from autogen_agentchat.messages import AgentEvent
from autogen_core import (
    AgentId,
    AgentRuntime,
    CancellationToken,
    ComponentBase,
    SingleThreadedAgentRuntime,
    try_get_known_serializers_for_type,
)
from clients.client import set_gomtm_api_context
from clients.rest_client import AsyncRestApi
from loguru import logger
from mtmai import loader
from mtmai.agents._types import ApiSaveTeamState, ApiSaveTeamTaskResult
from mtmai.agents.hf_space_agent import HfSpaceAgent
from mtmai.agents.webui_agent import UIAgent
from mtmai.clients.rest.api.mtmai_api import MtmaiApi
from mtmai.clients.rest.api_client import ApiClient
from mtmai.clients.rest.configuration import Configuration
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.clients.rest.models.chat_message import ChatMessage
from mtmai.clients.rest.models.chat_message_upsert import ChatMessageUpsert

# from mtmai.clients.rest.models.task_result import TaskResult
from mtmai.clients.rest.models.team_component import TeamComponent
from mtmai.context.context import Context, set_api_token_context, set_backend_url
from mtmai.core.config import settings
from mtmai.hatchet import Hatchet
from pydantic import BaseModel
from typing_extensions import Self


class WorkerAgentConfig(BaseModel):
    name: str
    # model_client: ComponentModel
    # tools: List[ComponentModel] | None
    # handoffs: List[HandoffBase | str] | None = None
    # model_context: ComponentModel | None = None
    # memory: List[ComponentModel] | None = None
    description: str
    system_message: str | None = None
    model_client_stream: bool = False
    reflect_on_tool_use: bool
    tool_call_summary_format: str


class WorkerAgent(Team, ComponentBase[WorkerAgentConfig]):
    """
    参考 autogen 的 BaseGroupChat 的实现方式
    """

    component_type = "worker"

    def __init__(self):
        self.backend_url = settings.GOMTM_URL
        if not self.backend_url:
            raise ValueError("backend_url is not set")
        self.worker = None
        self.autogen_host = None
        self.wfapp = None
        self.api_client = ApiClient(
            configuration=Configuration(
                host=self.backend_url,
            )
        )
        set_backend_url(self.backend_url)
        self._initialized = False
        self._is_running = False

        # Create a runtime for the team.
        # TODO: The runtime should be created by a managed context.
        self._runtime = SingleThreadedAgentRuntime()
        # Constants for the closure agent to collect the output messages.
        self._stop_reason: str | None = None
        self._output_message_queue: asyncio.Queue[AgentEvent | ChatMessage | None] = (
            asyncio.Queue()
        )

    async def _init(self, runtime: AgentRuntime) -> None:
        await self.start_autogen_host()
        ui_agent_id = AgentId("ui_agent", "default")
        ui_agent = await UIAgent.register(
            runtime=self._runtime,
            type=ui_agent_id.type,
            factory=lambda: UIAgent(description="ui_agent", wfapp=self.wfapp),
        )

        team_builder_id = AgentId("team_builder_agent", "default")
        self.worker_agent = await TeamBuilderAgent.register(
            runtime=self._runtime,
            type=team_builder_id.type,
            factory=lambda: TeamBuilderAgent(
                description=team_builder_id.type,
                ui_agent=ui_agent_id,
                wfapp=self.wfapp,
            ),
        )

        hf_space_agent_id = AgentId("hf_space_agent", "default")

        await HfSpaceAgent.register(
            runtime=self._runtime,
            type=hf_space_agent_id.type,
            factory=lambda: HfSpaceAgent(
                description=hf_space_agent_id.type,
                wfapp=self.wfapp,
            ),
        )
        self._initialized = True

    async def run(
        self,
        *,
        task: str | ChatMessage | Sequence[ChatMessage] | None = None,
        cancellation_token: CancellationToken | None = None,
    ) -> TaskResult:
        result: TaskResult | None = None
        if not self._initialized:
            await self._init(self._runtime)
        self._runtime.start()

        await self._init_ingestor()
        logger.info("worker agent 结束")

    async def handle_message(self, message: AgentRunInput):
        """处理外部消息,包括用户输入的消息"""
        ui_agent_id = AgentId("ui_agent", "default")
        await self._runtime.send_message(message=message, recipient=ui_agent_id)

    async def _init_ingestor(self):
        """食入外部消息,包括用户输入的消息"""
        maxRetry = settings.WORKER_MAX_RETRY
        for i in range(maxRetry):
            try:
                mtmaiapi = MtmaiApi(self.api_client)
                workerConfig = await mtmaiapi.mtmai_worker_config()
                os.environ["HATCHET_CLIENT_TLS_STRATEGY"] = "none"
                os.environ["HATCHET_CLIENT_TOKEN"] = workerConfig.token
                os.environ["DISPLAY"] = ":1"
                config_loader = loader.ConfigLoader(".")
                clientConfig = config_loader.load_client_config(
                    loader.ClientConfig(
                        server_url=settings.GOMTM_URL,
                        host_port=workerConfig.grpc_host_port,
                        tls_config=loader.ClientTLSConfig(
                            tls_strategy="none",
                            cert_file="None",
                            key_file="None",
                            ca_file="None",
                            server_name="localhost",
                        ),
                        # 绑定 python 默认logger,这样,就可以不用依赖 hatchet 内置的ctx.log()
                        # logger=logger,
                    )
                )
                token = clientConfig.token
                set_api_token_context(token)
                self.gomtmapi = AsyncRestApi(
                    host=settings.GOMTM_URL,
                    api_key=workerConfig.token,
                    tenant_id=clientConfig.tenant_id,
                )

                self.wfapp = Hatchet.from_config(
                    clientConfig,
                    debug=True,
                )

                self.worker = self.wfapp.worker(settings.WORKER_NAME)
                await self.setup_hatchet_workflows()

                logger.info("connect gomtm server success")
                break

            except Exception as e:
                if i == maxRetry - 1:
                    sys.exit(1)
                logger.info(f"failed to connect gomtm server, retry {i + 1},err:{e}")
                await asyncio.sleep(settings.WORKER_INTERVAL)
        # 非阻塞启动
        # self.worker.setup_loop(asyncio.new_event_loop())
        # asyncio.create_task(self.worker.async_start())
        # 阻塞启动
        await self.worker.async_start()

    async def start_autogen_host(self):
        from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntimeHost

        self.autogen_host = GrpcWorkerAgentRuntimeHost(address=settings.AG_HOST_ADDRESS)
        self.autogen_host.start()

    async def stop(self):
        if self.worker:
            await self.worker.async_stop()
            if self.autogen_host:
                await self.autogen_host.stop()
            if self.runtime:
                await self.runtime.stop()
            logger.warning("worker and autogen host stopped")

    async def setup_hatchet_workflows(self):
        wfapp = self.wfapp
        worker_app = self

        @wfapp.workflow(
            name="ag",
            on_events=["ag:run"],
            input_validator=AgentRunInput,
        )
        class FlowAg:
            @self.wfapp.step(timeout="60m")
            async def step_entry(self, hatctx: Context):
                set_gomtm_api_context(hatctx.aio)
                input = cast(AgentRunInput, hatctx.workflow_input())
                if not input.run_id:
                    input.run_id = hatctx.workflow_run_id()
                if not input.step_run_id:
                    input.step_run_id = hatctx.step_run_id
                return await worker_app.handle_message(input)

        self.worker.register_workflow(FlowAg())

    async def setup_browser_workflows(self):
        @self.wfapp.workflow(
            on_events=["browser:run"],
            # input_validator=CrewAIParams,
        )
        class FlowBrowser:
            @self.wfapp.step(timeout="10m", retries=1)
            async def run(self, hatctx: Context):
                from mtmai.clients.rest.models import BrowserParams

                # from mtmai.agents.browser_agent import BrowserAgent

                input = BrowserParams.model_validate(hatctx.workflow_input())
                # init_mtmai_context(hatctx)

                # ctx = get_mtmai_context()
                # tenant_id = ctx.tenant_id
                # llm_config = await wfapp.rest.aio.llm_api.llm_get(
                #     tenant=tenant_id, slug="default"
                # )
                # llm = ChatOpenAI(
                #     model=llm_config.model,
                #     api_key=llm_config.api_key,
                #     base_url=llm_config.base_url,
                #     temperature=0,
                #     max_tokens=40960,
                #     verbose=True,
                #     http_client=httpx.Client(transport=LoggingTransport()),
                #     http_async_client=httpx.AsyncClient(transport=LoggingTransport()),
                # )

                # 简单测试llm 是否配置正确
                # aa=llm.invoke(["Hello, how are you?"])
                # print(aa)
                # agent = BrowserAgent(
                #     generate_gif=False,
                #     use_vision=False,
                #     tool_call_in_content=False,
                #     # task="Navigate to 'https://en.wikipedia.org/wiki/Internet' and scroll down by one page - then scroll up by 100 pixels - then scroll down by 100 pixels - then scroll down by 10000 pixels.",
                #     task="Navigate to 'https://en.wikipedia.org/wiki/Internet' and to the string 'The vast majority of computer'",
                #     llm=llm,
                #     browser=Browser(config=BrowserConfig(headless=False)),
                # )
                # await agent.run()

        self.worker.register_workflow(FlowBrowser())

    async def reset(self) -> None:
        if not self._initialized:
            raise RuntimeError(
                "The group chat has not been initialized. It must be run before it can be reset."
            )

        if self._is_running:
            raise RuntimeError(
                "The group chat is currently running. It must be stopped before it can be reset."
            )
        self._is_running = True
        self._runtime.start()

        try:
            # Send a reset messages to all participants.
            # for participant_topic_type in self._participant_topic_types:
            #     await self._runtime.send_message(
            #         GroupChatReset(),
            #         recipient=AgentId(type=participant_topic_type, key=self._team_id),
            #     )
            # # Send a reset message to the group chat manager.
            # await self._runtime.send_message(
            #     GroupChatReset(),
            #     recipient=AgentId(type=self._group_chat_manager_topic_type, key=self._team_id),
            # )
            # from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime
            # grpc_runtime = GrpcWorkerAgentRuntime(host_address=settings.AG_HOST_ADDRESS)
            self._runtime = SingleThreadedAgentRuntime()

            message_serializer_types = [
                AgentRunInput,
                ChatMessage,
                ChatMessageUpsert,
                TeamComponent,
                # TaskResult,
                ApiSaveTeamState,
                ApiSaveTeamTaskResult,
            ]
            for message_serializer_type in message_serializer_types:
                self._runtime.add_message_serializer(
                    try_get_known_serializers_for_type(message_serializer_type)
                )

        finally:
            # Stop the runtime.
            await self._runtime.stop_when_idle()

            # Reset the output message queue.
            self._stop_reason = None
            while not self._output_message_queue.empty():
                self._output_message_queue.get_nowait()

            # Indicate that the team is no longer running.
            self._is_running = False

    async def save_state(self) -> Mapping[str, Any]:
        """Save the state of the group chat team."""
        if not self._initialized:
            raise RuntimeError(
                "The group chat has not been initialized. It must be run before it can be saved."
            )

        if self._is_running:
            raise RuntimeError("The team cannot be saved while it is running.")
        self._is_running = True

        try:
            # Save the state of the runtime. This will save the state of the participants and the group chat manager.
            agent_states = await self._runtime.save_state()
            # return TeamState(agent_states=agent_states, team_id=self._team_id).model_dump()

        finally:
            # Indicate that the team is no longer running.
            self._is_running = False

    async def load_state(self, state: Mapping[str, Any]) -> None:
        """Load the state of the group chat team."""
        if not self._initialized:
            await self._init(self._runtime)

        if self._is_running:
            raise RuntimeError("The team cannot be loaded while it is running.")
        self._is_running = True

        try:
            # Load the state of the runtime. This will load the state of the participants and the group chat manager.
            # team_state = TeamState.model_validate(state)
            # self._team_id = team_state.team_id
            # await self._runtime.load_state(team_state.agent_states)
            pass
        finally:
            # Indicate that the team is no longer running.
            self._is_running = False

    def _to_config(self) -> WorkerAgentConfig:
        participants = [
            participant.dump_component() for participant in self._participants
        ]
        termination_condition = (
            self._termination_condition.dump_component()
            if self._termination_condition
            else None
        )
        return WorkerAgentConfig(
            participants=participants,
            termination_condition=termination_condition,
            max_turns=self._max_turns,
        )

    @classmethod
    def _from_config(cls, config: WorkerAgentConfig) -> Self:
        # participants = [ChatAgent.load_component(participant) for participant in config.participants]
        # termination_condition = (
        #     TerminationCondition.load_component(config.termination_condition) if config.termination_condition else None
        # )
        return cls(max_turns=config.max_turns)
