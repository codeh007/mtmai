from __future__ import annotations

from typing import cast

from autogen_core import SingleThreadedAgentRuntime
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.context.context import Context
from mtmai.teams.sys_team import SysTeam
from mtmai.worker_app import mtmapp
from opentelemetry.trace import TracerProvider


@mtmapp.workflow(
    name="ag",
    on_events=["ag:run"],
)
class FlowAg:
    def __init__(self, tracer_provider: TracerProvider | None = None) -> None:
        self._runtime = SingleThreadedAgentRuntime(
            tracer_provider=tracer_provider,
            # payload_serialization_format=self._payload_serialization_format,
        )

    @mtmapp.step(timeout="60m")
    async def step_entry(self, hatctx: Context):
        input = AgentRunInput.model_validate(hatctx.input)
        message = cast(AgentRunInput, input)
        task = message.content
        sys_team = SysTeam()
        return await sys_team.run(task=task, cancellation_token=MtCancelToken())
