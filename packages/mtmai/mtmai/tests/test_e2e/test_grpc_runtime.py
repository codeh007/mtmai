# import os

from typing import TypedDict

import pytest
from mtmai.context.context import Context
from mtmai.hatchet import Hatchet
from mtmai.worker.worker import Worker

# from dotenv import load_dotenv

# envFileAbsPath = os.path.abspath("../gomtm/env/mtmai.env")
# load_dotenv(envFileAbsPath)
# gomtm_host_addr = "http://localhost:8383"


@pytest.mark.asyncio
async def test_example(mtmapp: Hatchet) -> None:
    assert mtmapp is not None

    worker = mtmapp.worker("testing_worker")

    await setup_hatchet_workflows(mtmapp, worker)


async def setup_hatchet_workflows(wfapp: Hatchet, worker: Worker):
    class MyResultType(TypedDict):
        my_func: str

    @wfapp.function(
        name="my_func2232",
    )
    def my_func(context: Context) -> MyResultType:
        return MyResultType(my_func="testing123")

    # @wfapp.workflow(
    #     name="ag",
    #     on_events=["ag:run"],
    #     input_validator=AgentRunInput,
    # )
    # class FlowAg:
    #     @wfapp.step(timeout="60m")
    #     async def step_entry(self, hatctx: Context):
    #         set_gomtm_api_context(hatctx.aio)
    #         input = cast(AgentRunInput, hatctx.workflow_input())
    #         if not input.run_id:
    #             input.run_id = hatctx.workflow_run_id()
    #         if not input.step_run_id:
    #             input.step_run_id = hatctx.step_run_id

    #         # agent_rpc_client = AgentRpcClient(self.config.server_url)
    #         runtime = GrpcWorkerAgentRuntime(agent_rpc_client=wfapp.client.ag)
    #         worker_team = WorkerTeam(client=wfapp.client)
    #         task_result = await worker_team.handle_message(input)
    #         return {
    #             "ok": True,
    #         }

    # worker.register_workflow(FlowAg())
    # print(f"Mtmapp instance: {mtmapp}")
