from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import TextMessage, ThoughtEvent
from clients.rest.models.team_run import TeamRun
from loguru import logger
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.chat_message_upsert import ChatMessageUpsert
from mtmai.clients.rest.models.flow_names import FlowNames
from mtmai.context.context import Context
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx, get_tenant_id
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name=FlowNames.TEAM,
    on_events=[f"{FlowNames.TEAM}"],
)
class FlowTeam:
    @mtmapp.step(timeout="60m")
    async def entry(self, hatctx: Context):
        input = TeamRun.model_validate(hatctx.input)
        cancellation_token = MtCancelToken()
        tenant_client = TenantClient()
        session_id = get_chat_session_id_ctx()
        tid = get_tenant_id()
        if not tid:
            raise ValueError("tenant_id is required")
        team = await tenant_client.ag.get_team_v2(
            tenant=tid,
            team_id=input.component_id,
        )

        # load team state
        # agState = await tenant_client.ag.load_team_state(
        #     tenant_id=tid,
        #     chat_id=session_id,
        # )
        # if agState:
        #     logger.info(f"load team state: {agState}")
        #     await team.load_state(agState)

        task_result = None
        async for event in team.run_stream(
            task=input.content,
            cancellation_token=cancellation_token,
        ):
            if cancellation_token and cancellation_token.is_cancelled():
                break
            if isinstance(event, TaskResult):
                task_result = event
                break
            # await tenant_client.emit(event)
            elif isinstance(event, TextMessage):
                await tenant_client.ag.chat_api.chat_message_upsert(
                    tenant=tid,
                    chat_message_upsert=ChatMessageUpsert(
                        tenant_id=tid,
                        content=event.content,
                        thread_id=session_id,
                        role=event.source,
                        source=event.source,
                        message_type="text",
                        threadId=session_id,
                    ),
                )
            elif isinstance(event, ThoughtEvent):
                await tenant_client.ag.chat_api.chat_message_upsert(
                    tenant=tid,
                    chat_message_upsert=ChatMessageUpsert(
                        tenant_id=tid,
                        content=event.content,
                        thread_id=session_id,
                        role=event.source,
                        source=event.source,
                        threadId=session_id,
                        message_type="thought",
                    ),
                )
            else:
                logger.warning(f"(FlowAg.run_stream)不支持的消息类型: {type(event)}")
        if team and hasattr(team, "_participants"):
            for agent in team._participants:
                if hasattr(agent, "close"):
                    await agent.close()

        await tenant_client.ag.save_team_state(
            componentId=input.component_id,
            tenant_id=tid,
            chat_id=session_id,
            state=await team.save_state(),
        )

        logger.info(f"(FlowAg)工作流结束,{hatctx.step_run_id}\n{task_result}")
        return task_result
