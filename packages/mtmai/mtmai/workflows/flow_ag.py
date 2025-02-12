import logging
from typing import cast

from mtmai.ag.agents._types import MessageChunk

from mtmai.ag.agents.webui_agent import UIAgent
from agents.ctx import AgentContext
from mtmaisdk.clients.rest.models.ag_event_create import AgEventCreate
from mtmaisdk.clients.rest.models.agent_run_input import AgentRunInput
from mtmaisdk.clients.rest.models.flow_ag_payload import FlowAgPayload
from mtmaisdk.context.context import Context
from pydantic import BaseModel

from mtmai.agents.ctx import get_mtmai_context, init_mtmai_context
from mtmai.worker import wfapp

from typing import cast

from mtmai.ag.agents.tenant_agent import TenantAgent
from mtmaisdk.clients.rest.models.tenant_seed_req import TenantSeedReq
from agents.ctx import AgentContext
from mtmaisdk.clients.rest.models.agent_run_input import AgentRunInput
from mtmaisdk.clients.rest.models.team import Team
from mtmaisdk.clients.rest.models.team_component import TeamComponent
from mtmaisdk.context.context import Context

from mtmai.ag.team_builder.company_research import CompanyResearchTeamBuilder
from mtmai.agents.ctx import get_mtmai_context, init_mtmai_context
from mtmai.worker import wfapp
from autogen_core import AgentId, SingleThreadedAgentRuntime, TypeSubscription
from autogen_core import TopicId
from autogen_core import RoutedAgent, message_handler, type_subscription
from autogen_agentchat.messages import TextMessage
from mtmai.ag.team_runner import TeamRunner
from rich.console import Console
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
        team_runner = TeamRunner()
        async for event in team_runner.run_stream(input):
            _event = event
            if isinstance(event, BaseModel):
                _event = event.model_dump()
            result = await hatctx.rest_client.aio.ag_events_api.ag_event_create(
                tenant=input.tenant_id,
                ag_event_create=AgEventCreate(
                    data=_event,
                    framework="autogen",
                    stepRunId=hatctx.step_run_id,
                    meta={},
                ),
            )
            hatctx.log(result)
            hatctx.put_stream(event)

        # 新版功能
        runtime = SingleThreadedAgentRuntime()

        runtime.start()
        ui_agent_type = await UIAgent.register(
            runtime,
            "ui_agent",
            lambda: UIAgent(
                on_message_chunk_func=send_cl_stream,
            ),
        )
        # 发布消息触发实际的 agent 运行
        Console().print(Markdown("Starting **`UI Agent`**"))

        await runtime.add_subscription(
            TypeSubscription(topic_type=config.ui_agent.topic_type, agent_type=ui_agent_type.type)
        )  # TODO: This could be a great example of using agent_id to route to sepecific element in the ui. Can replace MessageChunk.message_id


        await runtime.stop_when_idle()
        await runtime.close()

        return {"result": "success"}
