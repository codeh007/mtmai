from autogen_agentchat.teams import MagenticOneGroupChat
from autogen_agentchat.ui import Console
from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_core.models import ChatCompletionClient
from autogen_ext.agents.web_surfer import MultimodalWebSurfer
from loguru import logger
from mtmai.agents._agents import MtAssistantAgent
from mtmai.agents._types import TeamRunnerTask


class TeamRunnerAgent(RoutedAgent):
    def __init__(self, description: str, model_client: ChatCompletionClient) -> None:
        super().__init__(description)
        self._model_client = model_client

    @message_handler
    async def handle_run_team(
        self, message: TeamRunnerTask, ctx: MessageContext
    ) -> None:
        logger.info("(TeamRunnerTask)")
        task = message.task
        assistant = MtAssistantAgent(
            "Assistant",
            model_client=self._model_client,
        )

        surfer = MultimodalWebSurfer(
            "WebSurfer",
            model_client=self._model_client,
        )

        team = MagenticOneGroupChat(
            [assistant, surfer], model_client=self._model_client
        )
        await Console(
            team.run_stream(task="Provide a different proof for Fermat's Last Theorem")
        )

        # task = message.task
        # team_id = message.team_id
        # chat_id = message.chat_id

        # logger.info(f"{'-'*80}\nUser login, session ID: {self.id.key}.", flush=True)
        # # Get the user's initial input after login.
        # user_input = input("User: ")
        # logger.info(f"{'-'*80}\n{self.id.type}:\n{user_input}")
        # await self.publish_message(
        #     UserTask(context=[UserMessage(content=user_input, source="User")]),
        #     topic_id=TopicId(self._agent_topic_type, source=self.id.key),
        # )

        # tenant_client = TenantClient()
        # tid = tenant_client.tenant_id
        # if task.startswith("/tenant/seed"):
        #     logger.info("通知 TanantAgent 初始化(或重置)租户信息")
        #     result = await self._runtime.send_message(
        #         MsgResetTenant(tenant_id=tid),
        #         self.tenant_agent_id,
        #     )
        #     return

        # team_id = get_team_id_ctx() or generate_uuid()
        # chat_id = get_chat_session_id_ctx() or generate_uuid()
        # team = await tenant_client.ag.get_team()
        # ag_state = await tenant_client.ag.load_team_state(
        #     tenant_id=tenant_client.tenant_id,
        #     chat_id=chat_id,
        # )
        # if ag_state:
        #     await team.load_state(ag_state.state)

        # logger.info(f"运行: task: {task}, chat_id:{chat_id}")

        # await tenant_client.emit(
        #     ChatSessionStartEvent(
        #         threadId=chat_id,
        #     )
        # )

        # try:
        #     async for event in team.run_stream(
        #         task=task,
        #         cancellation_token=ctx.cancellation_token,
        #     ):
        #         if ctx.cancellation_token and ctx.cancellation_token.is_cancelled():
        #             break
        #         # yield event
        #         await tenant_client.event.emit(event)

        # finally:
        #     await tenant_client.ag.save_team_state(
        #         team=team,
        #         team_id=team_id,
        #         tenant_id=tenant_client.tenant_id,
        #         chat_id=chat_id,
        #     )

        # return
