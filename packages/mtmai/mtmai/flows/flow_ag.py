from loguru import logger
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
        # return await hatctx.sys_team.run_stream(
        #     task=AgentRunInput.model_validate(hatctx.input),
        #     cancellation_token=MtCancelToken(),
        # )

        input = AgentRunInput.model_validate(hatctx.input)
        cancellation_token = MtCancelToken()
        await hatctx.sys_team.run_team(input, cancellation_token)
        logger.info(f"(FlowResource)工作流结束,{hatctx.step_run_id}")
