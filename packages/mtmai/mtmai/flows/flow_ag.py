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
        return await hatctx.sys_team.run(
            task=AgentRunInput.model_validate(hatctx.input),
            cancellation_token=MtCancelToken(),
        )
