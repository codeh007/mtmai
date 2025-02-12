import logging
from typing import cast

from mtmai.agents._types import MessageChunk

from mtmai.agents.webui_agent import UIAgent
from agents.ctx import AgentContext
from mtmaisdk.clients.rest.models.agent_run_input import AgentRunInput
from mtmaisdk.context.context import Context
from pydantic import BaseModel

from mtmai.agents.ctx import get_mtmai_context, init_mtmai_context
from mtmai.worker import wfapp

from typing import cast
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime

from mtmai.agents.tenant_agent import TenantAgent
from mtmaisdk.clients.rest.models.tenant_seed_req import TenantSeedReq
from agents.ctx import AgentContext
from mtmaisdk.clients.rest.models.agent_run_input import AgentRunInput
from mtmaisdk.clients.rest.models.team import Team
from mtmaisdk.context.context import Context

from mtmai.agents.ctx import get_mtmai_context, init_mtmai_context
from mtmai.worker import wfapp
from autogen_core import  SingleThreadedAgentRuntime, TypeSubscription
from autogen_core import TopicId
from rich.console import Console
from mtmai.core.config import settings
from rich.markdown import Markdown

logger = logging.getLogger(__name__)


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



@wfapp.workflow(
    name="ag",
    on_events=["ag:run"],
    input_validator=AgentRunInput,
)
class FlowAg:
    @wfapp.step(
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


        # await grpc_runtime.stop_when_idle()
        await grpc_runtime.stop()

        return {"result": "success"}


@wfapp.workflow(
    name="tenant",
    on_events=["tenant:run"],
    input_validator=TenantSeedReq,
)
class FlowTenant:
    """
    租户工作流
    """

    @wfapp.step(
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



# @wfapp.workflow(
#     on_events=["agent:call"],
#     # input_validator=AgentNodeRunRequest,
# )
# class FlowRecovery:
#     """FlowRecovery"""

#     @wfapp.step(timeout="10m", retries=1)
#     async def run(self, hatctx: Context):
#         init_mtmai_context(hatctx)
#         input = cast(AgentNodeRunRequest, hatctx.workflow_input())
#         hatctx.log(f"input: {input}")

#         if input.flow_name == "crewai":
#             params = CrewAIParams()
#             hatctx.log("调用子工作流")
#             try:
#                 await hatctx.aio.spawn_workflow(
#                     FlowCrewAIAgent.__name__, params.model_dump()
#                 )
#             except Exception as e:
#                 # Spawn a recovery workflow
#                 await hatctx.aio.spawn_workflow("recovery-workflow", {"error": str(e)})
#             return {"next": "step_a1"}
#         elif input.flow_name == "scrape":
#             return {"next": "step_b1"}
#         # return await StepCallAgent(hatctx).run()
#         return {
#             "next": "step_a1",
#         }
