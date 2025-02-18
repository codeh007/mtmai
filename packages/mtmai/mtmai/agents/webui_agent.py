import time
from pathlib import Path
from typing import Any, Callable, Mapping, Optional, Union

from autogen_agentchat.base import Team
from autogen_agentchat.messages import TextMessage
from autogen_core import (
    Component,
    ComponentModel,
    MessageContext,
    RoutedAgent,
    default_subscription,
    message_handler,
)
from loguru import logger
from pydantic import BaseModel

from mtmai.agents._types import ApiSaveTeamState, ApiSaveTeamTaskResult
from mtmai.agents.model_client import MtmOpenAIChatCompletionClient
from mtmai.clients.rest.models.ag_state_upsert import AgStateUpsert
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.clients.rest.models.chat_message_upsert import ChatMessageUpsert
from mtmai.clients.rest.models.task_result import TaskResult
from mtmai.context.context import get_tenant_id, set_tenant_id
from mtmai.hatchet import Hatchet
from mtmai.mtlibs.id import generate_uuid
from mtmai.team_builder import assisant_team_builder

from ..clients.rest.models.mt_component import MtComponent


@default_subscription
class UIAgent(RoutedAgent):
    """
    UI Agent 是 UI 和 Worker 之间的桥梁, 负责处理 UI 发送的消息,
        1: 将状态通过SSE 推送到web 前端,
        2: 将消息和状态持久化到数据库
    """

    def __init__(self, description: str, wfapp: Hatchet = None) -> None:
        super().__init__(description)
        if wfapp is not None:
            self.wfapp = wfapp
            self.gomtmapi = self.wfapp.rest.aio

    async def load_state(self, state: Mapping[str, Any]) -> None:
        """Load the state of the group chat team."""
        self.last_message = state["last_message"]

    @message_handler
    async def handle_message_create(
        self, message: ChatMessageUpsert, ctx: MessageContext
    ) -> None:
        await self.gomtmapi.chat_api.chat_message_upsert(
            tenant=message.tenant_id,
            chat_message_upsert=message.model_dump(),
            # chat_message_upsert=ChatMessageUpsert(
            #     tenantId=message.tenant_id,
            #     componentId=message.component_id,
            #     content=message.content,
            #     role=message.role,
            #     threadId=message.thread_id,
            # ).model_dump(),
        )

    @message_handler
    async def on_new_message(self, message: AgentRunInput, ctx: MessageContext) -> None:
        start_time = time.time()
        logger.info(f"WorkerMainAgent 收到消息: {message}")
        tenant_id: str | None = message.tenant_id
        if not tenant_id:
            tenant_id = get_tenant_id()
        if not tenant_id:
            raise ValueError("tenant_id is required")
        set_tenant_id(tenant_id)
        run_id = message.run_id
        if not run_id:
            raise ValueError("run_id is required")

        user_input = message.content
        if user_input.startswith("/tenant/seed"):
            logger.info(f"通知 TanantAgent 初始化(或重置)租户信息: {message}")
            return

        team_comp_data: MtComponent = None
        if not message.team_id:
            assistant_team_builder = assisant_team_builder.AssistantTeamBuilder()
            team_comp_data = await self.get_or_create_default_team(
                tenant_id=message.tenant_id,
                label=assistant_team_builder.name,
            )
            message.team_id = team_comp_data.metadata.id

        thread_id = message.session_id
        if not thread_id:
            thread_id = generate_uuid()
        # team_component_data: MtComponent = await self.handle_tenant_message(
        #     MsgGetTeam(
        #         tenant_id=tenant_id,
        #         team_id=message.team_id,
        #     ),
        #     ctx,
        # )
        self.team = Team.load_component(team_comp_data.component)
        team_id = message.team_id
        if not team_id:
            team_id = generate_uuid()
        try:
            async for event in self.team.run_stream(
                task=message.content,
                cancellation_token=ctx.cancellation_token,
            ):
                if ctx.cancellation_token and ctx.cancellation_token.is_cancelled():
                    break

                if isinstance(event, TaskResult):
                    await self.handle_api_save_team_task_result(
                        ApiSaveTeamTaskResult(
                            tenant_id=tenant_id,
                            component_id=team_id,
                            task_result=event,
                        ),
                        ctx,
                    )
                elif isinstance(event, TextMessage):
                    await self.handle_message_create(
                        ChatMessageUpsert(
                            content=event.content,
                            tenant_id=message.tenant_id,
                            component_id=message.team_id,
                            threadId=thread_id,
                            runId=run_id,
                        ),
                        ctx,
                    )
                elif isinstance(event, BaseModel):
                    await self.handle_message_create(
                        ChatMessageUpsert(
                            content=event.model_dump_json(),
                            tenant_id=message.tenant_id,
                            component_id=message.team_id,
                        ),
                        ctx,
                    )
                else:
                    logger.info(f"WorkerMainAgent 收到(未知类型)消息: {event}")
        finally:
            await self.handle_api_save_team_state(
                ApiSaveTeamState(
                    tenant_id=tenant_id,
                    componentId=team_id,
                    state=await self.team.save_state(),
                    runId=run_id,
                ),
                ctx,
            )

    @message_handler
    async def handle_task_result(
        self, message: TaskResult, ctx: MessageContext
    ) -> None:
        logger.info("TODO: TaskResult")

    @message_handler
    async def handle_api_save_team_state(
        self, message: ApiSaveTeamState, ctx: MessageContext
    ) -> None:
        """保存团队状态"""
        logger.info("保存团队状态")
        # 确保停止团队的内部 agents
        if self.team and hasattr(self.team, "_participants"):
            for agent in self.team._participants:
                if hasattr(agent, "close"):
                    await agent.close()

        await self.gomtmapi.ag_state_api.ag_state_upsert(
            tenant=message.tenant_id,
            ag_state_upsert=AgStateUpsert(
                componentId=message.componentId,
                runId=message.runId,
                state=message.state,
            ).model_dump(),
        )

    @message_handler
    async def handle_api_save_team_task_result(
        self, message: ApiSaveTeamTaskResult, ctx: MessageContext
    ) -> None:
        """保存团队最终结果"""
        logger.info("TODO:UI Agent 保存任务结果")

    # @message_handler
    # async def handle_tenant_message(
    #     self, message: MsgGetTeam, mctx: MessageContext
    # ) -> MtComponent:
    #     tenant_id = message.tenant_id

    #     team_builters = [
    #         TravelTeamBuilder(),
    #         CompanyResearchTeamBuilder(),
    #         assisant_team_builder.AssistantTeamBuilder(),
    #     ]
    #     defaultModel = await self.gomtmapi.model_api.model_get(
    #         tenant=tenant_id, model="default"
    #     )
    #     model_dict = defaultModel.config.model_dump()
    #     model_dict.pop("n", None)
    #     model_client = MtmOpenAIChatCompletionClient(
    #         **model_dict,
    #     )
    #     for team_builder in team_builters:
    #         team = await team_builder.create_team(model_client)
    #         team_comp = team.dump_component()
    #         comp = TeamComponent(**team_comp.model_dump())
    #         team2 = MtComponent(
    #             label=team_comp.label,
    #             description=team_comp.description or "",
    #             component=comp.model_dump(),
    #         )
    #         logger.info(
    #             f"create team for tenant: {message.tenant_id}, team: {team._team_id}"
    #         )
    #         await self.gomtmapi.coms_api.coms_upsert(
    #             tenant=message.tenant_id,
    #             com=team._team_id,
    #             mt_component=team2.model_dump(),
    #         )
    #     comps = await self.gomtmapi.coms_api.coms_list(tenant=tenant_id)
    #     detault_team_item = next(
    #         (
    #             item
    #             for item in comps.rows
    #             if item.label == assisant_team_builder.AssistantTeamBuilder().name
    #         ),
    #         None,
    #     )

    #     return await self.gomtmapi.coms_api.coms_get(
    #         tenant=tenant_id,
    #         com=detault_team_item.metadata.id,
    #     )

    async def _create_team_component(
        self,
        team_config: Union[str, Path, dict, ComponentModel],
        input_func: Optional[Callable] = None,
    ) -> Component:
        """Create team instance from config"""
        if isinstance(team_config, (str, Path)):
            config = await self.load_from_file(team_config)
        elif isinstance(team_config, dict):
            config = team_config
        else:
            config = team_config.model_dump()

        team = Team.load_component(config)

        for agent in team._participants:
            if hasattr(agent, "input_func"):
                agent.input_func = input_func

        return team

    async def get_or_create_default_team(self, tenant_id: str, label: str):
        teams_list = await self.gomtmapi.coms_api.coms_list(
            tenant=tenant_id, label=label
        )
        if teams_list.rows and len(teams_list.rows) > 0:
            logger.info(f"获取到默认聊天团队 {teams_list.rows[0].metadata.id}")
            return teams_list.rows[0]
        else:
            logger.info(f"create default team for tenant {tenant_id}")
            defaultModel = await self.gomtmapi.model_api.model_get(
                tenant=tenant_id, model="default"
            )
            model_dict = defaultModel.config.model_dump()
            model_dict.pop("n", None)
            # model_dict["model_info"] = model_dict.pop("model_info", None)
            model_client = MtmOpenAIChatCompletionClient(
                **model_dict,
            )

            default_team_builder = assisant_team_builder.AssistantTeamBuilder()
            team_comp = await default_team_builder.create_team(model_client)
            component_model = team_comp.dump_component()
            comp = component_model.model_dump()
            team_component = MtComponent(
                label=component_model.label,
                description=component_model.description or "",
                componentType="team",
                component=comp,
            )
            logger.info(f"create default team for tenant {tenant_id}")
            new_team = await self.gomtmapi.coms_api.coms_upsert(
                tenant=tenant_id,
                com=generate_uuid(),
                mt_component=team_component.model_dump(),
            )
            return new_team
