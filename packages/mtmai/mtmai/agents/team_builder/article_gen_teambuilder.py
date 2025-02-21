from typing import Sequence

from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import MaxMessageTermination
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_agentchat.teams import SelectorGroupChat
from autogen_core.models import ChatCompletionClient

from ..tools.web_search import search_web_tool

# from .__init__ import current_team_version


def percentage_change_tool(start: float, end: float) -> float:
    return ((end - start) / start) * 100


class ArticleGenTeamBuilder:
    """默认AI助理团"""

    @property
    def name(self):
        return "article_gen_team"

    @property
    def description(self):
        return "文章生成团队"

    async def create_team(self, default_model_client: ChatCompletionClient = None):
        # By default, AssistantAgent returns the tool output as the response.
        # If your tool does not return a well-formed string in natural language format,
        # you may want to add a reflection step within the agent by setting reflect_on_tool_use=True when creating the agent.
        # This will allow the agent to reflect on the tool output and provide a natural language response.
        planning_agent = AssistantAgent(
            "PlanningAgent",
            description="An agent for planning tasks, this agent should be the first to engage when given a new task.",
            model_client=default_model_client,
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
        web_search_agent = AssistantAgent(
            "WebSearchAgent",
            description="An agent for searching information on the web.",
            tools=[search_web_tool],
            model_client=default_model_client,
            system_message="""
            You are a web search agent.
            Your only tool is search_tool - use it to find information.
            You make only one search call at a time.
            Once you have the results, you never do calculations based on them.
            """,
        )

        # 提示: 不要加:"TERMINATE" 这个条件,因为团队的相关agents自己会提及 "TERMINATE",
        # 团队成员提及 "TERMINATE" 时, 会自动终止团队
        max_messages_termination = MaxMessageTermination(max_messages=25)
        termination = max_messages_termination

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

        user_proxy_agent = UserProxyAgent(
            "UserProxyAgent",
            description="A proxy for the user to approve or disapprove tasks.",
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
            [planning_agent, web_search_agent],
            model_client=default_model_client,
            termination_condition=termination,
            selector_prompt=selector_prompt,
            allow_repeated_speaker=True,  # Allow an agent to speak multiple turns in a row.
            # selector_func=selector_func,  # 可选,(自定义选择器)
            selector_func=selector_func_with_user_proxy,  # 选择器: 由用户确认后继续执行 planer 安排的任务
        )
        # team.component_version = current_team_version
        team.component_label = self.name
        team.component_description = self.description
        return team
