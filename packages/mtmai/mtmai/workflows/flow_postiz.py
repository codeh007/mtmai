from typing import cast

from mtmaisdk.clients.rest.models import PostizState
from mtmaisdk.context.context import Context

from mtmai.agents.ctx import init_mtmai_context
from mtmai.agents.postiz_graph import postiz_graph
from mtmai.worker import wfapp


# 参考：
# https://github.com/gitroomhq/postiz-app/blob/main/libraries/nestjs-libraries/src/agent/agent.graph.service.ts
@wfapp.workflow(
    name="postiz",
    on_events=["postiz:run"],
    # input_validator=PostizState,
)
class FlowPostiz:
    @wfapp.step(timeout="10m", retries=1)
    async def step_entry(self, hatctx: Context):
        init_mtmai_context(hatctx)

        input: PostizState = cast(PostizState, hatctx.workflow_input())
        outoput = await postiz_graph.PostizGraph.run(input)

        return {**outoput}
