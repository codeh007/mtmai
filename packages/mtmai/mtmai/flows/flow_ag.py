from __future__ import annotations

from typing import cast

from mtmai.agents.worker_agent.worker_team import WorkerTeam
from mtmai.clients.agent_runtime.mtm_runtime import GrpcWorkerAgentRuntime
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.context.context import Context
from mtmai.hatchet import step
from mtmpb import ag_connecpy


class FlowAg:
    @step(timeout="60m")
    async def step_entry(self, hatctx: Context):
        input = cast(AgentRunInput, hatctx.workflow_input())
        if not input.run_id:
            input.run_id = hatctx.workflow_run_id()
        if not input.step_run_id:
            input.step_run_id = hatctx.step_run_id

        # agent_rpc_client = AgentRpcClient(self.config.server_url)
        ag_connecpy.AsyncAgServiceClient
        runtime = GrpcWorkerAgentRuntime(agent_rpc_client=hatctx.aio.ag)

        worker_team = WorkerTeam(hatctx=hatctx)
        task_result = await worker_team.handle_message(input)
        return {
            "ok": True,
        }
