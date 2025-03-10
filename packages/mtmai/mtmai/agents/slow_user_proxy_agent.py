from dataclasses import dataclass
from typing import Any, Mapping

from autogen_core import DefaultTopicId, MessageContext, RoutedAgent, message_handler
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.models import AssistantMessage


@dataclass
class TextMessage:
    source: str
    content: str


@dataclass
class UserTextMessage(TextMessage):
    pass


@dataclass
class AssistantTextMessage(TextMessage):
    pass


@dataclass
class GetSlowUserMessage:
    content: str


@dataclass
class TerminateMessage:
    content: str


class MockPersistence:
    def __init__(self):
        self._content: Mapping[str, Any] = {}

    def load_content(self) -> Mapping[str, Any]:
        return self._content

    def save_content(self, content: Mapping[str, Any]) -> None:
        self._content = content


state_persister = MockPersistence()


# @type_subscription("scheduling_assistant_conversation")
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
        await self.publish_message(
            GetSlowUserMessage(content=message.content),
            topic_id=DefaultTopicId("scheduling_assistant_conversation"),
        )

    async def save_state(self) -> Mapping[str, Any]:
        state_to_save = {
            "memory": await self._model_context.save_state(),
        }
        return state_to_save

    async def load_state(self, state: Mapping[str, Any]) -> None:
        await self._model_context.load_state(state["memory"])
