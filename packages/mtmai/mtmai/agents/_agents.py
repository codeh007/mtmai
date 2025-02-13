from dataclasses import dataclass
from typing import List
from autogen_core import Component, DefaultTopicId, MessageContext, RoutedAgent, default_subscription, message_handler
from autogen_agentchat.agents._user_proxy_agent import UserProxyAgentConfig
from autogen_agentchat.agents import UserProxyAgent
from autogen_agentchat.base import ChatAgent, TerminationCondition
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.teams._group_chat._round_robin_group_chat import (
    RoundRobinGroupChatConfig,
)
from autogen_core import (
    AgentId,
    DefaultSubscription,
    DefaultTopicId,
    MessageContext,
    RoutedAgent,
    message_handler,
)
from autogen_ext.runtimes.grpc import GrpcWorkerAgentRuntime

from ._types import AskToGreet, CascadingMessage, Feedback, Greeting, ReceiveMessageEvent

class ReceiveAgent(RoutedAgent):
    def __init__(self) -> None:
        super().__init__("Receive Agent")

    @message_handler
    async def on_greet(self, message: Greeting, ctx: MessageContext) -> Greeting:
        return Greeting(content=f"Received: {message.content}")

    @message_handler
    async def on_feedback(self, message: Feedback, ctx: MessageContext) -> None:
        print(f"Feedback received: {message.content}")


class GreeterAgent(RoutedAgent):
    def __init__(self, receive_agent_type: str) -> None:
        super().__init__("Greeter Agent")
        self._receive_agent_id = AgentId(receive_agent_type, self.id.key)

    @message_handler
    async def on_ask(self, message: AskToGreet, ctx: MessageContext) -> None:
        response = await self.send_message(Greeting(f"Hello, {message.content}!"), recipient=self._receive_agent_id)
        await self.publish_message(Feedback(f"Feedback: {response.content}"), topic_id=DefaultTopicId())



@default_subscription
class WorkerMainAgent(RoutedAgent):
    def __init__(self, max_rounds: int) -> None:
        super().__init__("A cascading agent.")
        self.max_rounds = max_rounds

    @message_handler
    async def on_new_message(self, message: CascadingMessage, ctx: MessageContext) -> None:
        await self.publish_message(
            ReceiveMessageEvent(round=message.round, sender=str(ctx.sender), recipient=str(self.id)),
            topic_id=DefaultTopicId(),
        )
        if message.round == self.max_rounds:
            return
        await self.publish_message(CascadingMessage(round=message.round + 1), topic_id=DefaultTopicId())



class MtWebUserProxyAgent(UserProxyAgent):
    """扩展 UserProxyAgent"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def _to_config(self) -> UserProxyAgentConfig:
        # TODO: Add ability to serialie input_func
        return UserProxyAgentConfig(name=self.name, description=self.description, input_func=None)

class MtRoundRobinGroupChatConfig(RoundRobinGroupChatConfig):
    """扩展 RoundRobinGroupChatConfig"""

    # user_proxy_agent_name: str = "user_proxy_agent"
    pass


class MtRoundRobinGroupChat(
    RoundRobinGroupChat, Component[MtRoundRobinGroupChatConfig]
):
    """扩展 RoundRobinGroupChat"""

    component_provider_override = (
        "mtmai.ag.base.RoundRobinGroupChat.MtRoundRobinGroupChat"
    )

    def __init__(
        self,
        participants: List[ChatAgent],
        termination_condition: TerminationCondition | None = None,
        max_turns: int | None = None,
    ):
        # 检查是否已经包含 user_proxy_agent
        # has_user_proxy = False
        # for participant in participants:
        #     if isinstance(participant, MtWebUserProxyAgent):
        #         has_user_proxy = True
        #         break

        # if not has_user_proxy:
        #     participants = [
        #         MtWebUserProxyAgent(
        #             name="user_proxy_agent",
        #         )
        #     ] + participants
        super().__init__(participants, termination_condition, max_turns)


async def main() -> None:
    runtime = GrpcWorkerAgentRuntime(host_address="localhost:50051")
    runtime.start()

    await ReceiveAgent.register(
        runtime,
        "receiver",
        lambda: ReceiveAgent(),
    )
    await runtime.add_subscription(DefaultSubscription(agent_type="receiver"))
    await GreeterAgent.register(
        runtime,
        "greeter",
        lambda: GreeterAgent("receiver"),
    )
    await runtime.add_subscription(DefaultSubscription(agent_type="greeter"))
    await runtime.publish_message(AskToGreet("Hello World!"), topic_id=DefaultTopicId())

    await runtime.stop_when_signal()