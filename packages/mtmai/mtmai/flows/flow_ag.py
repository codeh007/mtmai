from __future__ import annotations

from dataclasses import dataclass
from typing import cast

from autogen_core import (
    AgentId,
    DefaultSubscription,
    DefaultTopicId,
    MessageContext,
    RoutedAgent,
    message_handler,
)
from mtmai.agents.worker_team import WorkerTeam
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.context.context import Context
from mtmai.worker_app import mtmapp

from ..agents.rpc_demo_team import RpcDemoTeam
from ..clients.agent_runtime.mtm_runtime import MtmAgentRuntime


@dataclass
class AskToGreet:
    content: str


@dataclass
class Greeting:
    content: str


@dataclass
class Feedback:
    content: str


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
        response = await self.send_message(
            Greeting(f"Hello, {message.content}!"), recipient=self._receive_agent_id
        )
        await self.publish_message(
            Feedback(f"Feedback: {response.content}"), topic_id=DefaultTopicId()
        )


@mtmapp.workflow(
    name="ag",
    on_events=["ag:run"],
    input_validator=AgentRunInput,
)
class FlowAg:
    @mtmapp.step()
    async def step_entry(self, hatctx: Context):
        # runtime = MtmAgentRuntime(host_address="localhost:8383")
        # await runtime.start()
        # runtime = mtmapp.agent_runtime
        runtime = hatctx.worker.agent_runtime
        # runtime.start()
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
        await runtime.publish_message(
            AskToGreet("Hello World!"), topic_id=DefaultTopicId()
        )

        await runtime.stop_when_signal()

        input = cast(AgentRunInput, hatctx.workflow_input())
        if not input.run_id:
            input.run_id = hatctx.workflow_run_id()
        if not input.step_run_id:
            input.step_run_id = hatctx.step_run_id

        # aaa = hatctx.admin.run(my_durable_func, {"test": "test-durable"})
        # print(aaa)

        # runtime = MtmAgentRuntime(agent_rpc_client=hatctx.aio.ag)

        _runtime = MtmAgentRuntime(agent_rpc_client=hatctx.aio.ag)

        rpc_demo_team = RpcDemoTeam(_runtime)
        await rpc_demo_team.run()

        worker_team = WorkerTeam(hatctx=hatctx)
        task_result = await worker_team.run(input)
        return {
            "ok": True,
        }
