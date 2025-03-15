from autogen_agentchat.base import TaskResult, Team
from autogen_core import (
    AgentRuntime,
    MessageContext,
    RoutedAgent,
    SingleThreadedAgentRuntime,
    message_handler,
)
from loguru import logger
from mtmai.agents.intervention_handlers import NeedsUserInputHandler
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.clients.rest.models.chat_session_start_event import ChatSessionStartEvent
from mtmai.clients.rest.models.component_types import ComponentTypes
from mtmai.clients.rest.models.mt_task_result import MtTaskResult
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_tenant_id, set_step_canceled_ctx
from mtmai.teams.instagram_team import InstagramTeam


class TeamRunnerAgent(RoutedAgent):
    def __init__(self, description: str) -> None:
        super().__init__(description)
        self.teams: list[Team] = []

    @message_handler
    async def run_team(self, message: AgentRunInput, ctx: MessageContext) -> None:
        # logger.info(f"(TeamRunnerTask), resource_id: {message.resource_id}")
        set_step_canceled_ctx(False)
        tenant_client = TenantClient()
        session_id = self.id.key

        agState = await tenant_client.ag.load_team_state(
            tenant_id=tenant_client.tenant_id,
            chat_id=session_id,
        )
        logger.info(f"agState: {agState}")
        needs_user_input_handler = NeedsUserInputHandler()
        runtime = SingleThreadedAgentRuntime(
            intervention_handlers=[needs_user_input_handler]
        )

        runtime.start()

        team = await self.build_team(runtime=runtime, component_id=message.component_id)
        await tenant_client.emit(ChatSessionStartEvent(threadId=session_id))
        self.teams.append(team)

        ######################################################################################
        # 提示:
        # 1:团队的结束不等于 runtime 的结束
        # 2: runtime 可以复用
        # 3: 可以使用 外置的 持久 agent 参与到临时组建的团队
        ######################################################################################
        async for event in team.run_stream(
            task=message.content,
            cancellation_token=ctx.cancellation_token,
        ):
            if isinstance(message, TaskResult):
                result = message
                mt_result = MtTaskResult(
                    messages=result.messages,
                    stop_reason=result.stop_reason,
                )
                tenant_client.emit(mt_result)
                break
            await tenant_client.emit(event)

        await tenant_client.ag.save_team_state(
            team=team,
            component_id=message.component_id,
            tenant_id=tenant_client.tenant_id,
            chat_id=session_id,
        )

        await runtime.stop_when_idle()
        logger.info("团队运行完全结束")

    async def build_team(self, runtime: AgentRuntime, component_id: str | None = None):
        tenant_client = TenantClient()
        tid = get_tenant_id()
        if not tid:
            raise ValueError("tenant_id is required")
        component_data = await tenant_client.ag.coms_api.coms_get(
            tenant=tid,
            com=component_id,
        )
        logger.info(f"component data: {component_data}")

        if component_data.component_type == ComponentTypes.TEAM:
            # team = Team.load_component(component_data)
            team = InstagramTeam.load_component(component_data)
            if isinstance(team, InstagramTeam):
                return team
            else:
                raise ValueError(f"不支持组件类型: {component_data.component_type}")
        else:
            raise ValueError(f"不支持组件类型: {component_data.component_type}")
