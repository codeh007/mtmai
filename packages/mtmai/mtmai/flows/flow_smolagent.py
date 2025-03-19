from loguru import logger
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.clients.rest.models.flow_names import FlowNames
from mtmai.context.context import Context
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name=FlowNames.SMOLA,
    on_events=[f"{FlowNames.SMOLA}"],
)
class FlowSmolagent:
    @mtmapp.step(timeout="60m")
    async def smolagent_entry(self, hatctx: Context):
        input = AgentRunInput.model_validate(hatctx.input)
        cancellation_token = MtCancelToken()
        from smolagents import CodeAgent, DuckDuckGoSearchTool, HfApiModel

        model = HfApiModel()
        agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=model)

        result = agent.run(
            "How many seconds would it take for a leopard at full speed to run through Pont des Arts?"
        )
        logger.info(f"result: {result}")

        return {"output": "Hello, FlowSmolagent!"}
