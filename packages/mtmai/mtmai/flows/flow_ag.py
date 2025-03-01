from __future__ import annotations

from typing import cast

from autogen_core import DefaultTopicId

from mtmai.agents.greeter_team import AskToGreet
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.context.context import Context
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name="ag",
    on_events=["ag:run"],
    input_validator=AgentRunInput,
)
class FlowAg:
    @mtmapp.step()
    async def step_entry(self, hatctx: Context):
        # conn = hatctx.agent_runtime_client
        # runtime = MtmAgentRuntime(config=hatctx.config)
        # await runtime.start()
        # 提示: hatctx.worker.agent_runtime 是全局的.
        # runtime = hatctx.worker.agent_runtime

        input = cast(AgentRunInput, hatctx.workflow_input())
        if not input.run_id:
            input.run_id = hatctx.workflow_run_id()
        if not input.step_run_id:
            input.step_run_id = hatctx.step_run_id

        # worker_team = WorkerTeam(hatctx=hatctx)
        # task_result = await worker_team.run(input)
        ag_runtime = hatctx.ag_runtime
        await ag_runtime.publish_message(
            AskToGreet("Hello World!"), topic_id=DefaultTopicId()
        )
        return {
            "ok": True,
        }
