from typing import Any

from autogen_core import AgentId, RoutedAgent, default_subscription

from mtmai.hatchet import Hatchet


@default_subscription
class TeamBuilderAgent(RoutedAgent):
    """
    应用总代理(单例)
    主要功能:
    1. 管理应用的全局状态,包括,重置全局应用状态
    2. 根据团队配置，创建团队
    """

    def __init__(self, description: str, wfapp: Hatchet = None) -> None:
        if wfapp is not None:
            self.wfapp = wfapp
            self.gomtmapi = self.wfapp.rest.aio
        # if ui_agent is not None:
        #     self.ui_agent = ui_agent
        else:
            raise ValueError("ui_agent is required")
        # self.team_builder = [
        #     AssistantTeamBuilder(),
        #     SwramTeamBuilder(),
        # ]
        super().__init__(description)

    # async def _create_team_component(
    #     self,
    #     team_config: Union[str, Path, dict, ComponentModel],
    #     input_func: Optional[Callable] = None,
    # ) -> Component:
    #     """Create team instance from config"""
    #     if isinstance(team_config, (str, Path)):
    #         config = await self.load_from_file(team_config)
    #     elif isinstance(team_config, dict):
    #         config = team_config
    #     else:
    #         config = team_config.model_dump()

    #     team = Team.load_component(config)

    #     for agent in team._participants:
    #         if hasattr(agent, "input_func"):
    #             agent.input_func = input_func

    #     return team

    # @message_handler
    # async def on_new_message(self, message: AgentRunInput, ctx: MessageContext) -> None:
    #     start_time = time.time()
    #     logger.info(f"WorkerMainAgent 收到消息: {message}")
    #     tenant_id: str | None = message.tenant_id
    #     if not tenant_id:
    #         tenant_id = get_tenant_id()
    #     if not tenant_id:
    #         raise ValueError("tenant_id is required")
    #     set_tenant_id(tenant_id)
    #     run_id = message.run_id
    #     if not run_id:
    #         raise ValueError("run_id is required")

    #     user_input = message.content
    #     if user_input.startswith("/tenant/seed"):
    #         logger.info(f"通知 TanantAgent 初始化(或重置)租户信息: {message}")
    #         # await self.runtime.publish_message(
    #         #     TenantSeedReq(tenantId=tenant_id),
    #         #     topic_id=DefaultTopicId(),
    #         # )
    #         return

    #     ag_helper = AgHelper(self.gomtmapi)
    #     if not message.team_id:
    #         assistant_team_builder = AssistantTeamBuilder()
    #         team = await ag_helper.get_or_create_default_team(
    #             tenant_id=message.tenant_id,
    #             label=assistant_team_builder.name,
    #         )
    #         message.team_id = team.metadata.id

    #     thread_id = message.session_id
    #     if not thread_id:
    #         thread_id = generate_uuid()

    #     team_component_data: Team = await self.send_ui_msg(
    #         MsgGetTeam(
    #             tenant_id=tenant_id,
    #             team_id=message.team_id,
    #         )
    #     )
    #     # team.
    #     team = Team.load_component(team_component_data.component.model_dump())
    #     team_id = message.team_id
    #     if not team_id:
    #         team_id = generate_uuid()
    #     try:
    #         async for event in team.run_stream(
    #             task=message.content,
    #             cancellation_token=ctx.cancellation_token,
    #         ):
    #             if ctx.cancellation_token and ctx.cancellation_token.is_cancelled():
    #                 break
    #             try:
    #                 if isinstance(event, TaskResult):
    #                     await self.send_ui_msg(
    #                         ApiSaveTeamTaskResult(
    #                             tenant_id=tenant_id,
    #                             team_id=team_id,
    #                             task_result=event,
    #                         ),
    #                     )
    #                 elif isinstance(event, TextMessage):
    #                     await self.send_ui_msg(
    #                         ChatMessageUpsert(
    #                             content=event.content,
    #                             tenant_id=message.tenant_id,
    #                             team_id=message.team_id,
    #                             threadId=thread_id,
    #                             runId=run_id,
    #                         ),
    #                     )
    #                 elif isinstance(event, BaseModel):
    #                     await self.send_ui_msg(
    #                         ChatMessageUpsert(
    #                             content=event.model_dump_json(),
    #                             tenant_id=message.tenant_id,
    #                             team_id=message.team_id,
    #                         ),
    #                     )
    #                     # await self.send_ui_msg(
    #                     #     AgEventCreate(
    #                     #         data=event,
    #                     #         framework="autogen",
    #                     #         meta={},
    #                     #     ),
    #                     # )
    #                 else:
    #                     logger.info(f"WorkerMainAgent 收到(未知类型)消息: {event}")
    #             except Exception as e:
    #                 logger.error(f"WorkerMainAgent stream 运行出错: {e}")

    #     except Exception as e:
    #         logger.error(f"WorkerMainAgent 运行出错: {e}")
    #         raise e
    #     finally:
    #         # 确保停止团队的内部 agents
    #         if team and hasattr(team, "_participants"):
    #             for agent in team._participants:
    #                 if hasattr(agent, "close"):
    #                     await agent.close()

    #         result = await self.send_ui_msg(
    #             ApiSaveTeamState(
    #                 tenant_id=tenant_id,
    #                 team_id=team_id,
    #                 state=await team.save_state(),
    #                 componentId=team_id,
    #                 runId=run_id,
    #             ),
    #         )
    #         return result

    # @message_handler
    # async def start_web_server(self, message: MsgStartWebServer, ctx: MessageContext):
    #     """启动web服务"""
    #     # from mtmai.core.logging import get_logger
    #     # from mtmai.server import serve

    #     # logger = get_logger()
    #     # logger.info("🚀 start web server : %s:%s", settings.HOSTNAME, settings.PORT)
    #     # asyncio.run(serve())
    #     return {"message": "TODO: start web server"}

    # @message_handler
    # async def handle_ag_event(
    #     self, message: AgEventCreate, ctx: MessageContext
    # ) -> None:
    #     logger.info("TODO: AgEventCreate")

    async def send_ui_msg(self, message: Any):
        """发送UI消息

        Args:
            *messages: 可变参数,支持发送多条消息
        """
        target_agent_id = AgentId(type="ui_agent", key="default")
        return await self.send_message(
            message=message,
            recipient=target_agent_id,
        )

        # 学习:
        # 如果消息没法本智能体处理,应抛出异常: CantHandleException
