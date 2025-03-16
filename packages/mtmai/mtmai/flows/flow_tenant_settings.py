from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.clients.rest.models.flow_names import FlowNames
from mtmai.context.context import Context
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name=FlowNames.TENANT_SETTINGS,
    on_events=[f"{FlowNames.TENANT_SETTINGS}"],
)
class FlowTenantSettings:
    @mtmapp.step(timeout="60m")
    async def step_tenant_settings_entry(self, hatctx: Context):
        input = AgentRunInput.model_validate(hatctx.input)
        return {
            "tenant_settings": "reset",
        }
