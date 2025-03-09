from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.context.context import Context
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name="platform_account",
    on_events=["platform_account:run"],
)
class FlowPlatformAccount:
    @mtmapp.step(timeout="60m")
    async def step_entry(self, hatctx: Context):
        return await hatctx.sys_team.run_stream(
            task=AgentRunInput.model_validate(hatctx.input),
            cancellation_token=MtCancelToken(),
        )
