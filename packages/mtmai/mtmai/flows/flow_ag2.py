from __future__ import annotations

from autogen_core import DefaultTopicId, SingleThreadedAgentRuntime
from mtmai.agents.greeter_team import AskToGreet
from mtmai.context.context import Context
from mtmai.worker_app import mtmapp
from opentelemetry.trace import TracerProvider


@mtmapp.workflow(
    name="ag2",
    on_events=["ag2:run"],
)
class FlowAg2:
    def __init__(self, tracer_provider: TracerProvider | None = None) -> None:
        self._runtime = SingleThreadedAgentRuntime(
            tracer_provider=tracer_provider,
            # payload_serialization_format=self._payload_serialization_format,
        )

    @mtmapp.step(timeout="60m")
    async def step_entry(self, ctx: Context):
        # input = AgentRunInput.model_validate(hatctx.input)
        # message = cast(AgentRunInput, input)
        # task = message.content
        # assisant_team = SysTeam()
        # return await assisant_team.run(task=task, cancellation_token=MtCancelToken())
        runtime = ctx.ag_runtime
        # await runtime.publish_message(AskToGreet("hello999"))
        # response = await runtime.send_message(
        #     AskToGreet("hello999"), recipient=self._receive_agent_id
        # )
        await runtime.publish_message(
            AskToGreet("Hello World!"), topic_id=DefaultTopicId()
        )
        return {"result": "ok"}
