import datetime
import json
from typing import Any, Mapping

from autogen_core import (
    CancellationToken,
    DefaultTopicId,
    FunctionCall,
    MessageContext,
    RoutedAgent,
    TopicId,
    message_handler,
)
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.models import (
    AssistantMessage,
    ChatCompletionClient,
    SystemMessage,
    UserMessage,
)
from autogen_core.tools import BaseTool
from mtmai.agents._agents import scheduling_assistant_topic_type
from mtmai.agents._types import (
    AssistantTextMessage,
    GetSlowUserMessage,
    ScheduleMeetingOutput,
    TerminateMessage,
    UserTextMessage,
)
from pydantic import BaseModel, Field


class MockPersistence:
    def __init__(self):
        self._content: Mapping[str, Any] = {}

    def load_content(self) -> Mapping[str, Any]:
        return self._content

    def save_content(self, content: Mapping[str, Any]) -> None:
        self._content = content


state_persister = MockPersistence()


class SlowUserProxyAgent(RoutedAgent):
    def __init__(
        self,
        name: str,
        description: str,
    ) -> None:
        super().__init__(description)
        self._model_context = BufferedChatCompletionContext(buffer_size=5)
        self._name = name

    @message_handler
    async def handle_message(
        self, message: AssistantTextMessage, ctx: MessageContext
    ) -> None:
        await self._model_context.add_message(
            AssistantMessage(content=message.content, source=message.source)
        )
        session_id = self.id.key
        await self.publish_message(
            GetSlowUserMessage(content=message.content),
            topic_id=TopicId(type=scheduling_assistant_topic_type, source=session_id),
        )

    async def save_state(self) -> Mapping[str, Any]:
        state_to_save = {
            "memory": await self._model_context.save_state(),
        }
        return state_to_save

    async def load_state(self, state: Mapping[str, Any]) -> None:
        await self._model_context.load_state(state["memory"])


class ScheduleMeetingInput(BaseModel):
    recipient: str = Field(description="Name of recipient")
    date: str = Field(description="Date of meeting")
    time: str = Field(description="Time of meeting")


class ScheduleMeetingTool(BaseTool[ScheduleMeetingInput, ScheduleMeetingOutput]):
    def __init__(self):
        super().__init__(
            ScheduleMeetingInput,
            ScheduleMeetingOutput,
            "schedule_meeting",
            "Schedule a meeting with a recipient at a specific date and time",
        )

    async def run(
        self, args: ScheduleMeetingInput, cancellation_token: CancellationToken
    ) -> ScheduleMeetingOutput:
        print(f"Meeting scheduled with {args.recipient} on {args.date} at {args.time}")
        return ScheduleMeetingOutput()


class SchedulingAssistantAgent(RoutedAgent):
    def __init__(
        self,
        name: str,
        description: str,
        model_client: ChatCompletionClient,
        initial_message: AssistantTextMessage | None = None,
    ) -> None:
        super().__init__(description)
        self._model_context = BufferedChatCompletionContext(
            buffer_size=5,
            initial_messages=[
                UserMessage(
                    content=initial_message.content, source=initial_message.source
                )
            ]
            if initial_message
            else None,
        )
        self._name = name
        self._model_client = model_client
        self._system_messages = [
            SystemMessage(
                content=f"""
I am a helpful AI assistant that helps schedule meetings.
If there are missing parameters, I will ask for them.

Today's date is {datetime.datetime.now().strftime("%Y-%m-%d")}
"""
            )
        ]

    @message_handler
    async def handle_message(
        self, message: UserTextMessage, ctx: MessageContext
    ) -> None:
        await self._model_context.add_message(
            UserMessage(content=message.content, source=message.source)
        )

        tools = [ScheduleMeetingTool()]
        response = await self._model_client.create(
            self._system_messages + (await self._model_context.get_messages()),
            tools=tools,
        )

        if isinstance(response.content, list) and all(
            isinstance(item, FunctionCall) for item in response.content
        ):
            for call in response.content:
                tool = next((tool for tool in tools if tool.name == call.name), None)
                if tool is None:
                    raise ValueError(f"Tool not found: {call.name}")
                arguments = json.loads(call.arguments)
                await tool.run_json(arguments, ctx.cancellation_token)
            await self.publish_message(
                TerminateMessage(content="Meeting scheduled"),
                topic_id=DefaultTopicId("scheduling_assistant_conversation"),
            )
            return

        assert isinstance(response.content, str)
        speech = AssistantTextMessage(
            content=response.content, source=self.metadata["type"]
        )
        await self._model_context.add_message(
            AssistantMessage(content=response.content, source=self.metadata["type"])
        )

        await self.publish_message(
            speech, topic_id=DefaultTopicId("scheduling_assistant_conversation")
        )

    async def save_state(self) -> Mapping[str, Any]:
        return {
            "memory": await self._model_context.save_state(),
        }

    async def load_state(self, state: Mapping[str, Any]) -> None:
        await self._model_context.load_state(state["memory"])
