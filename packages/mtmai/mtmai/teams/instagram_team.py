from typing import AsyncGenerator, List, Sequence

from autogen_agentchat.base import TaskResult, TerminationCondition
from autogen_agentchat.conditions import (
    MaxMessageTermination,
    SourceMatchTermination,
    StopMessageTermination,
    TextMentionTermination,
)
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_agentchat.teams import SelectorGroupChat
from autogen_core import AgentRuntime, CancellationToken, Component, ComponentModel
from loguru import logger
from mtmai.agents._agents import MtAssistantAgent
from mtmai.agents.model_client import MtmOpenAIChatCompletionClient
from mtmai.agents.termination import MyFunctionCallTermination
from pydantic import BaseModel


def wait_admin_approval(prompt: str) -> str:
    """等待管理员批准"""
    logger.info(f"等待管理员批准: {prompt}")
    return f"等待管理员批准: {prompt}"


class InstagramTeamConfig(BaseModel):
    participants: List[ComponentModel]
    termination_condition: ComponentModel | None = None
    max_turns: int | None = None
    some_value: str = "some_value"
    result_id: str = None


class InstagramTeam(SelectorGroupChat, Component[InstagramTeamConfig]):
    component_type = "mtmai.teams.instagram_team.InstagramTeam"

    def __init__(
        self,
        participants: List[ComponentModel] = [],
        model_client: MtmOpenAIChatCompletionClient | None = None,
        termination_condition: TerminationCondition | None = None,
        max_turns: int | None = None,
        runtime: AgentRuntime | None = None,
    ) -> None:
        test_assisant = MtAssistantAgent(
            name="test_assisant",
            description="test_assisant",
            model_client=model_client,
        )

        planning_agent = MtAssistantAgent(
            "PlanningAgent",
            description="An agent for planning tasks, this agent should be the first to engage when given a new task.",
            model_client=model_client,
            tools=[wait_admin_approval],
            system_message="""
            You are a planning agent.
            Your job is to break down complex tasks into smaller, manageable subtasks.
            Your team members are:
                WebSearchAgent: Searches for information
                DataAnalystAgent: Performs calculations

            You only plan and delegate tasks - you do not execute them yourself.

            When assigning tasks, use this format:
            1. <agent> : <task>

            生成了规划后, 等待管理员批准, 批准后, 继续执行规划的任务
            After all tasks are complete, summarize the findings and end with "TERMINATE".
            """,
        )
        participants.append(test_assisant)
        participants.append(planning_agent)

        instagram_assistant = MtAssistantAgent(
            "InstagramAssistant",
            description="An agent for instagram tasks.",
            model_client=model_client,
        )
        participants.append(instagram_assistant)

        # 可选
        def selector_func(messages: Sequence[AgentEvent | ChatMessage]) -> str | None:
            if messages[-1].source != planning_agent.name:
                return planning_agent.name
            return None

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

        super().__init__(
            participants=participants,
            termination_condition=termination,
            model_client=model_client,
            allow_repeated_speaker=True,
            max_turns=10,
            runtime=runtime,
            selector_prompt=selector_prompt,
        )

    async def run_stream(
        self,
        *,
        task: str | ChatMessage | Sequence[ChatMessage] | None = None,
        cancellation_token: CancellationToken | None = None,
    ) -> AsyncGenerator[AgentEvent | ChatMessage | TaskResult, None]:
        return super().run_stream(
            task=task,
            cancellation_token=cancellation_token,
        )
