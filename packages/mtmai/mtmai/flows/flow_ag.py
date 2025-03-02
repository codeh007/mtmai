from __future__ import annotations

from typing import cast

from mtmai.agents.worker_team import WorkerTeam
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.context.context import Context
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name="ag",
    on_events=["ag:run"],
    input_validator=AgentRunInput,
)
class FlowAg:
    @mtmapp.step(timeout="60m")
    async def step_entry(self, hatctx: Context):
        # conn = hatctx.agent_runtime_client
        # runtime = MtmAgentRuntime(config=hatctx.config)
        # await runtime.start()
        # 提示: hatctx.worker.agent_runtime 是全局的.
        # runtime = hatctx.worker.agent_runtime

        # set_step_run_id(hatctx.step_run_id)

        input = cast(AgentRunInput, hatctx.workflow_input())
        return await WorkerTeam().run(input)
