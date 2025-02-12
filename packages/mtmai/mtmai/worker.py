import asyncio
import logging
import os
import sys
from typing import cast
from mtmaisdk import ClientConfig, Hatchet, loader
from mtmaisdk.clients.rest import ApiClient
from mtmaisdk.clients.rest.api.mtmai_api import MtmaiApi
from mtmaisdk.clients.rest.configuration import Configuration
from autogen_core import DefaultTopicId, SingleThreadedAgentRuntime, TopicId, TypeSubscription, try_get_known_serializers_for_type
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime
from mtmai.core.config import settings
from autogen_core import RoutedAgent, default_subscription
from autogen_core import (
    AgentId,
    DefaultSubscription,
    DefaultTopicId,
    MessageContext,
    RoutedAgent,
    message_handler,
)

from .agents.tenant_agent import TenantAgent
from ..mtmaisdk.clients.rest.models.tenant_seed_req import TenantSeedReq

from .agents.webui_agent import UIAgent

from .agents.ctx import AgentContext, get_mtmai_context, init_mtmai_context
from ..mtmaisdk.context.context import Context
from ..mtmaisdk.clients.rest.models.agent_run_input import AgentRunInput

from .agents._types import CascadingMessage, MessageChunk
from rich.console import Console
from rich.markdown import Markdown

logger = logging.getLogger()

@default_subscription
class WorkerAgent(RoutedAgent):
    def __init__(self):
        self.backend_url = settings.GOMTM_URL
        if not self.backend_url:
            raise ValueError("backend_url is not set")
        self.worker = None
        self.autogen_host = None
        self.wfapp = None

    async def setup(self):
        self.api_client = ApiClient(
            configuration=Configuration(
                host=self.backend_url,
            )
        )

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
                    ClientConfig(
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
                        logger=logger,
                    )
                )
                self.wfapp = Hatchet.from_config(
                    clientConfig,
                    debug=True,
                )

                self.worker = self.wfapp.worker(settings.WORKER_NAME)
                await setup_hatchet_workflows(self)

                logger.info("connect gomtm server success")
                return

            except Exception as e:
                if i == maxRetry - 1:
                    sys.exit(1)
                logger.info(f"failed to connect gomtm server, retry {i+1},err:{e}")
                await asyncio.sleep(settings.WORKER_INTERVAL)
        raise ValueError("failed to connect gomtm server")

    async def deploy_workers(self):
        try:
            await self.setup()
            await self.start_autogen_host()
            await self.start_reveiver_agent()
            await self.worker.async_start()
        except Exception as e:
            logger.exception(f"failed to deploy workers: {e}")
            raise e


    @message_handler
    async def on_new_message(self, message: CascadingMessage, ctx: MessageContext) -> None:
        print(message)
        # await self.publish_message(
        #     ReceiveMessageEvent(round=message.round, sender=str(ctx.sender), recipient=str(self.id)),
        #     topic_id=DefaultTopicId(),
        # )
        # if message.round == self.max_rounds:
        #     return
        # await self.publish_message(CascadingMessage(round=message.round + 1), topic_id=DefaultTopicId())

    async def start_autogen_host(self):
        from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntimeHost
        self.autogen_host = GrpcWorkerAgentRuntimeHost(address=settings.AG_HOST_ADDRESS)
        self.autogen_host.start()
        logger.info(f"🟢 AG host at: {settings.AG_HOST_ADDRESS}")


    async def start_reveiver_agent(self):
        """
            作用:
                作为分布式,其他 agents 运行的过程不直接处理消息的日志, 前端界面的消息处理等数据.
                这里,通过 grpc 的方式,接收其他 agents 的日志, 前端界面的消息处理等数据.
        """
        from mtmai.agents._agents import ReceiveAgent
        from mtmai.agents._types import CascadingMessage
        self.autogen_worker_runtime = GrpcWorkerAgentRuntime(host_address=settings.AG_HOST_ADDRESS)
        self.autogen_worker_runtime.add_message_serializer(try_get_known_serializers_for_type(CascadingMessage))
        self.autogen_worker_runtime.start()

    async def stop(self):
        if self.worker:
            await self.worker.async_stop()
            if self.autogen_host:
                await self.autogen_host.stop()
            if self.autogen_worker_runtime:
                await self.autogen_worker_runtime.stop()
            logger.warning("worker and autogen host stopped")

async def send_cl_stream(msg: MessageChunk) -> None:
    print(msg)
    # if msg.message_id not in message_chunks:
    #     message_chunks[msg.message_id] = Message(content="", author=msg.author)

    # if not msg.finished:
    #     await message_chunks[msg.message_id].stream_token(msg.text)  # type: ignore [reportUnknownVariableType]
    # else:
    #     await message_chunks[msg.message_id].stream_token(msg.text)  # type: ignore [reportUnknownVariableType]
    #     await message_chunks[msg.message_id].update()  # type: ignore [reportUnknownMemberType]
    #     await asyncio.sleep(3)
    #     cl_msg = message_chunks[msg.message_id]  # type: ignore [reportUnknownVariableType]
    #     await cl_msg.send()  # type: ignore [reportUnknownMemberType]

async def setup_hatchet_workflows(worker_agent:WorkerAgent):
    logger.info("Setting up hatchet workflows...")

    @worker_agent.wfapp.workflow(
        name="ag",
        on_events=["ag:run"],
        input_validator=AgentRunInput,
    )
    class FlowAg:
        @worker_agent.wfapp.step(
            timeout="30m",
            # retries=1
        )
        async def step_entry(self, hatctx: Context):
            init_mtmai_context(hatctx)
            input = cast(AgentRunInput, hatctx.workflow_input())
            # 旧版功能
            # team_runner = TeamRunner()
            # async for event in team_runner.run_stream(input):
            #     _event = event
            #     if isinstance(event, BaseModel):
            #         _event = event.model_dump()
            #     result = await hatctx.rest_client.aio.ag_events_api.ag_event_create(
            #         tenant=input.tenant_id,
            #         ag_event_create=AgEventCreate(
            #             data=_event,
            #             framework="autogen",
            #             stepRunId=hatctx.step_run_id,
            #             meta={},
            #         ),
            #     )
            #     # hatctx.log(result)
            #     hatctx.put_stream(event)

            # 新版功能
            # runtime = SingleThreadedAgentRuntime()
            grpc_runtime = GrpcWorkerAgentRuntime(host_address=settings.AG_HOST_ADDRESS)

            grpc_runtime.start()
            ui_agent_type = await UIAgent.register(
                grpc_runtime,
                "ui_agent",
                lambda: UIAgent(
                    on_message_chunk_func=send_cl_stream,
                ),
            )
            Console().print(Markdown("Starting **`UI Agent`**"))

            await grpc_runtime.add_subscription(
                TypeSubscription(topic_type="uiagent", agent_type=ui_agent_type.type)
            )  # TODO: This could be a great example of using agent_id to route to sepecific element in the ui. Can replace MessageChunk.message_id

            await grpc_runtime.publish_message(CascadingMessage(round=1), topic_id=DefaultTopicId())

            # await grpc_runtime.stop_when_idle()
            await grpc_runtime.stop()

            return {"result": "success"}

    worker_agent.worker.register_workflow(FlowAg())


    @worker_agent.wfapp.workflow(
        name="tenant",
        on_events=["tenant:run"],
        input_validator=TenantSeedReq,
    )
    class FlowTenant:
        """
        租户工作流
        """

        @worker_agent.wfapp.step(
            timeout="30m",
            # retries=1
        )
        async def step_reset_tenant(self, hatctx: Context):
            init_mtmai_context(hatctx)
            ctx: AgentContext = get_mtmai_context()
            ctx.set_hatch_context(hatctx)
            input = cast(TenantSeedReq, hatctx.workflow_input())
            # 新版功能
            runtime = SingleThreadedAgentRuntime()
            await TenantAgent.register(runtime, "tenant_agent", lambda: TenantAgent(ctx))
            # await runtime.add_subscription(TypeSubscription(topic_type="tenant", agent_type="broadcasting_agent"))

            runtime.start()
            # await runtime.send_message(
            #     message=input,
            #     recipient=AgentId(type="tenant_agent", key="default"),
            # )
            # 广播方从而避免工作流中消息类型的相关转换问题.
            await runtime.publish_message(
                input,
                topic_id=TopicId(type="tenant", source="tenant"),
            )

            await runtime.stop_when_idle()  # This will block until the runtime is idle.
            await runtime.close()
            return {"result": "success"}
    worker_agent.worker.register_workflow(FlowTenant())