from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import TextMessage, ThoughtEvent
from loguru import logger
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.clients.rest.models.chat_message_upsert import ChatMessageUpsert
from mtmai.clients.rest.models.component_types import ComponentTypes
from mtmai.clients.rest.models.flow_names import FlowNames
from mtmai.context.context import Context
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx, get_tenant_id
from mtmai.teams.instagram_team import InstagramTeam
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name=FlowNames.AG,
    on_events=[f"{FlowNames.AG}"],
)
class FlowAg:
    @mtmapp.step(timeout="60m")
    async def step_entry(self, hatctx: Context):
        input = AgentRunInput.model_validate(hatctx.input)
        cancellation_token = MtCancelToken()
        tenant_client = TenantClient()
        session_id = get_chat_session_id_ctx()
        tid = get_tenant_id()
        if not tid:
            raise ValueError("tenant_id is required")
        try:
            component_data = await tenant_client.ag.coms_api.coms_get(
                tenant=tid,
                com=input.component_id,
            )
            logger.info(f"component data: {component_data}")
        except Exception as e:
            logger.exception(f"获取组件数据失败: {e}")
            raise e
        if component_data.component_type == ComponentTypes.TEAM:
            # if hasattr(component_data.config, "actual_instance"):
            #     # component_data.config.model_validate()(component_data.config.actual_instance)
            #     setattr(
            #         component_data.config,
            #         "actual_instance",
            #         component_data.config.actual_instance,
            #     )
            comp_dict = component_data.model_dump()
            # comp_dict["config"] = comp_dict["config"]["actual_instance"]
            # team = InstagramTeam.load_component(comp_dict)
            # comp_dict["config"] = aaa["actual_instance"].model_dump()
            team = InstagramTeam.load_component(comp_dict)
        else:
            raise ValueError(f"不支持组件类型: {component_data.component_type}")

        # load team state
        agState = await tenant_client.ag.load_team_state(
            tenant_id=tid,
            chat_id=session_id,
        )
        if agState:
            logger.info(f"load team state: {agState}")
            await team.load_state(agState)

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
                        source=session_id,
                        message_type="text",
                        threadId=session_id,
                        # topic=self._agent_topic_type,
                        # topic=ctx.topic_id.type,
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
                        source=session_id,
                        threadId=session_id,
                        message_type="thought",
                        # topic=self._agent_topic_type,
                        # topic=ctx.topic_id.type,
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
