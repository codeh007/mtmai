from typing import cast

from mtmai.agents.ctx import init_mtmai_context
from mtmai.worker import wfapp
from mtmai.workflows.flow_crewai import FlowCrewAIAgent
from mtmaisdk.clients.rest.models import AgentNodeRunRequest, CrewAIParams
from mtmaisdk.context.context import Context


@wfapp.workflow(
    on_events=["agent:call"],
    input_validator=AgentNodeRunRequest,
)
class FlowRecovery:
    """FlowRecovery"""

    @wfapp.step(timeout="10m", retries=1)
    async def run(self, hatctx: Context):
        init_mtmai_context(hatctx)
        input = cast(AgentNodeRunRequest, hatctx.workflow_input())
        hatctx.log(f"input: {input}")

        if input.flow_name == "crewai":
            params = CrewAIParams()
            hatctx.log("调用子工作流")
            try:
                await hatctx.aio.spawn_workflow(
                    FlowCrewAIAgent.__name__, params.model_dump()
                )
            except Exception as e:
                # Spawn a recovery workflow
                await hatctx.aio.spawn_workflow("recovery-workflow", {"error": str(e)})
            return {"next": "step_a1"}
        elif input.flow_name == "scrape":
            return {"next": "step_b1"}
        # return await StepCallAgent(hatctx).run()
        return {
            "next": "step_a1",
        }
