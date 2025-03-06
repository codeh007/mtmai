from __future__ import annotations

from typing import cast

from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.context.context import Context
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name="ag",
    on_events=["ag:run"],
)
class FlowAg:
    @mtmapp.step(timeout="60m")
    async def step_entry(self, hatctx: Context):
        input = AgentRunInput.model_validate(hatctx.input)
        message = cast(AgentRunInput, input)
        # task = message.content
        # team = TeamTeam()
        # team = DemoHandoffsTeam()
        return await hatctx.sys_team.run(
            task=message, cancellation_token=MtCancelToken()
        )
