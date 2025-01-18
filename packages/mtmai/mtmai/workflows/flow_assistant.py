from typing import cast

from mtmaisdk.clients.rest.models import PostizState
from mtmaisdk.context.context import Context

from mtmai.agents.assisant_graph import assisant_graph
from mtmai.agents.ctx import init_mtmai_context
from mtmai.worker import wfapp


@wfapp.workflow(
    name="assisant",
    on_events=["assisant:run"],
    # input_validator=PostizState,
)
class FlowAssistant:
    @wfapp.step(timeout="10m", retries=1)
    async def step_entry(self, hatctx: Context):
        init_mtmai_context(hatctx)

        input: PostizState = cast(PostizState, hatctx.workflow_input())
        outoput = await assisant_graph.AssistantGraph.run(input)

        return {**outoput}
