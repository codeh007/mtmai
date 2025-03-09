from typing import Sequence

from autogen_agentchat.conditions import (
    MaxMessageTermination,
    SourceMatchTermination,
    StopMessageTermination,
    TextMentionTermination,
)
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_agentchat.teams import SelectorGroupChat
from autogen_core.models import ChatCompletionClient
from mtmai.agents._agents import MtAssistantAgent
from mtmai.agents.termination import MyFunctionCallTermination
from mtmai.agents.user_agent import UserAgent


class InstagramTeamBuilder:
    """instagram团队"""

    @property
    def name(self):
        return "instagram_team"

    @property
    def description(self):
        return "instagram_team"

    async def create_team(
        self,
        # stop_condition: ExternalTermination | None = None,
        model_client: ChatCompletionClient = None,
    ):
        # tenant_client = TenantClient()
        # if not model_client:
        #     model_client = await tenant_client.ag.default_model_client(
        #         tenant_client.tenant_id
        #     )
        planning_agent = MtAssistantAgent(
            "PlanningAgent",
            description="An agent for planning tasks, this agent should be the first to engage when given a new task.",
            model_client=model_client,
            system_message="""
            You are a planning agent.
            Your job is to break down complex tasks into smaller, manageable subtasks.
            Your team members are:
                WebSearchAgent: Searches for information
                DataAnalystAgent: Performs calculations

            You only plan and delegate tasks - you do not execute them yourself.

            When assigning tasks, use this format:
            1. <agent> : <task>

            After all tasks are complete, summarize the findings and end with "TERMINATE".
            """,
        )

        # termination = TextMentionTermination(text="TERMINATE")
        # max_msg_termination = MaxMessageTermination(max_messages=6)
        # text_mention_termination = TextMentionTermination("TERMINATE")
        # 提示: 不要加:"TERMINATE" 这个条件,因为团队的相关agents自己会提及 "TERMINATE",
        # 团队成员提及 "TERMINATE" 时, 会自动终止团队
        max_messages_termination = MaxMessageTermination(max_messages=25)
        my_function_call_termination = MyFunctionCallTermination(
            function_name="TERMINATE"
        )
        source_termination = SourceMatchTermination(sources=["UserProxyAgent"])
        text_mention_termination = TextMentionTermination("TERMINATE")
        stop_termination = StopMessageTermination()
        termination = (
            max_messages_termination
            & my_function_call_termination
            & source_termination
            & stop_termination
        )

        selector_prompt = """Select an agent to perform task.

{roles}

Current conversation context:
{history}

Read the above conversation, then select an agent from {participants} to perform the next task.
Make sure the planner agent has assigned tasks before other agents start working.
Only select one agent.
"""

        # 可选
        def selector_func(messages: Sequence[AgentEvent | ChatMessage]) -> str | None:
            if messages[-1].source != planning_agent.name:
                return planning_agent.name
            return None

        user_proxy_agent = UserAgent(
            name="UserProxyAgent",
            description="A proxy for the user to approve or disapprove tasks.",
        )

        instagram_assistant = MtAssistantAgent(
            "InstagramAssistant",
            description="An agent for instagram tasks.",
            model_client=model_client,
        )

        def selector_func_with_user_proxy(
            messages: Sequence[AgentEvent | ChatMessage],
        ) -> str | None:
            if (
                messages[-1].source != planning_agent.name
                and messages[-1].source != user_proxy_agent.name
            ):
                # Planning agent should be the first to engage when given a new task, or check progress.
                return planning_agent.name
            if messages[-1].source == planning_agent.name:
                if (
                    messages[-2].source == user_proxy_agent.name
                    and "APPROVE" in messages[-1].content.upper()
                ):  # type: ignore
                    # User has approved the plan, proceed to the next agent.
                    return None
                # Use the user proxy agent to get the user's approval to proceed.
                return user_proxy_agent.name
            if messages[-1].source == user_proxy_agent.name:
                # If the user does not approve, return to the planning agent.
                if "APPROVE" not in messages[-1].content.upper():  # type: ignore
                    return planning_agent.name
            return None

        team = SelectorGroupChat(
            participants=[planning_agent, user_proxy_agent, instagram_assistant],
            model_client=model_client,
            termination_condition=termination,
            selector_prompt=selector_prompt,
            allow_repeated_speaker=True,  # Allow an agent to speak multiple turns in a row.
            # selector_func=selector_func,  # 可选,(自定义选择器)
            selector_func=selector_func_with_user_proxy,  # 选择器: 由用户确认后继续执行 planer 安排的任务
            max_turns=3,
        )
        # team.component_version = current_team_version
        team.component_label = self.name
        team.component_description = self.description
        return team
