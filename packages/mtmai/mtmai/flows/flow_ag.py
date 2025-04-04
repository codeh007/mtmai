from autogen_agentchat.base import Response
from autogen_agentchat.messages import (
    HandoffMessage,
    TextMessage,
    ToolCallExecutionEvent,
    ToolCallRequestEvent,
    ToolCallSummaryMessage,
)
from autogen_agentchat.teams import BaseGroupChat
from loguru import logger

from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.ag_state_upsert import AgStateUpsert
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.clients.rest.models.flow_names import FlowNames
from mtmai.clients.rest.models.state_type import StateType
from mtmai.clients.tenant_client import TenantClient
from mtmai.context.context import Context
from mtmai.context.ctx import get_chat_session_id_ctx, get_tenant_id
from mtmai.teams.social.social_team import SocialTeam
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name=FlowNames.AG,
    on_events=[f"{FlowNames.AG}"],
)
class FlowAg:
    @mtmapp.step(timeout="60m")
    async def step0(self, hatctx: Context):
        input = AgentRunInput.from_dict(hatctx.input)
        cancellation_token = MtCancelToken()
        tenant_client = TenantClient()
        session_id = get_chat_session_id_ctx()
        tid = get_tenant_id()
        if not tid:
            raise ValueError("tenant_id is required")

        task = input.content
        last_txt_message = ""
        team = await tenant_client.load_team(input.component_id)

        if isinstance(team, BaseGroupChat):
            output_stream = team.run_stream(
                task=task, cancellation_token=cancellation_token
            )
            async for message in output_stream:
                if isinstance(message, ToolCallRequestEvent):
                    for tool_call in message.content:
                        logger.info(
                            f"  [acting]! Calling {tool_call.name}... [/acting]"
                        )

                elif isinstance(message, ToolCallExecutionEvent):
                    for result in message.content:
                        # Compute formatted text separately to avoid backslashes in the f-string expression.
                        formatted_text = result.content[:200].replace("\n", r"\n")
                        logger.info(f"  [observe]> {formatted_text} [/observe]")

                elif isinstance(message, Response):
                    if isinstance(message.chat_message, TextMessage):
                        last_txt_message += message.chat_message.content
                    elif isinstance(message.chat_message, ToolCallSummaryMessage):
                        content = message.chat_message.content
                        # only print the first 100 characters
                        # console.print(Panel(content[:100] + "...", title="Tool(s) Result (showing only 100 chars)"))
                        last_txt_message += content
                    else:
                        raise ValueError(
                            f"Unexpected message type: {message.chat_message}"
                        )
                    logger.info(last_txt_message)
                elif isinstance(message, HandoffMessage):
                    logger.info(f"工作流收到 HandoffMessage: {message}")
                else:
                    logger.info(f"工作流收到其他消息: {message}")

            state = await team.save_state()
            await tenant_client.ag.save_team_state(
                componentId=input.component_id,
                tenant_id=tenant_client.tenant_id,
                chat_id=session_id,
                state=state,
            )
            await tenant_client.ag_state_api.ag_state_upsert(
                tenant=tenant_client.tenant_id,
                ag_state_upsert=AgStateUpsert(
                    componentId=input.component_id,
                    chatId=session_id,
                    state=state,
                    type=StateType.RUNTIMESTATE,
                ),
            )
        elif isinstance(team, SocialTeam):
            result = await team.run_stream(
                task=input, cancellation_token=cancellation_token
            )
            logger.info(f"team result: {result}")
        else:
            raise ValueError(f"Unexpected team type: {type(team)}")

        return {"state": "unknown"}
