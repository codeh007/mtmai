from clients.rest.models.run_flow_model_input import RunFlowModelInput
from model_client.model_client import MtOpenAIChatCompletionClient
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.context.context import Context
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx, get_tenant_id
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name="model",
    on_events=["model"],
)
class FlowModel:
    @mtmapp.step(timeout="10m")
    async def entry(self, hatctx: Context):
        input = RunFlowModelInput.model_validate(hatctx.input)
        cancellation_token = MtCancelToken()
        tenant_client = TenantClient()
        session_id = get_chat_session_id_ctx()
        tid = get_tenant_id()

        modelObj = await tenant_client.ag.model_api.model_get(model_id=input.model_id)
        model_client = MtOpenAIChatCompletionClient.load_component(modelObj)
        return {
            "status": "Manager ok, success",
        }
