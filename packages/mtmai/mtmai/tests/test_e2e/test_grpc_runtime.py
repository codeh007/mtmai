import base64
import time
from typing import cast

import pytest
from mtmai.agents.worker_agent.worker_team import WorkerTeam
from mtmai.clients.agent_runtime.mtm_runtime import GrpcWorkerAgentRuntime
from mtmai.clients.client import set_gomtm_api_context
from mtmai.context.context import Context
from mtmai.hatchet import Hatchet
from mtmai.mtmpb.ag_pb2 import AgentRunInput
from mtmai.worker.worker import Worker


@pytest.mark.asyncio
async def test_example(mtmapp: Hatchet, worker: Worker) -> None:
    assert mtmapp is not None
    await setup_example_workflows(mtmapp, worker)
    print("setup_example_workflows 完成")
    await setup_worker_2(mtmapp, worker)
    print("setup_worker_2 完成")


async def setup_example_workflows(wfapp: Hatchet, worker: Worker):
    # class MyResultType(TypedDict):
    #     my_func: str

    # @wfapp.function(
    #     name="my_func2232",
    # )
    # def my_func(context: Context) -> MyResultType:
    #     return MyResultType(my_func="testing123")

    @wfapp.workflow(
        name="test_ag",
        on_events=["test_ag:run"],
        # input_validator=AgentRunInput,
    )
    class FlowAg:
        @wfapp.step(timeout="60m")
        async def step_entry(self, hatctx: Context):
            set_gomtm_api_context(hatctx.aio)
            input = cast(AgentRunInput, hatctx.workflow_input())
            if not input.run_id:
                input.run_id = hatctx.workflow_run_id()
            if not input.step_run_id:
                input.step_run_id = hatctx.step_run_id

            # agent_rpc_client = AgentRpcClient(self.config.server_url)
            runtime = GrpcWorkerAgentRuntime(agent_rpc_client=wfapp.client.ag)
            worker_team = WorkerTeam(client=wfapp.client)
            task_result = await worker_team.handle_message(input)
            return {
                "ok": True,
            }

    # worker.register_workflow(FlowAg())
    # print(f"Mtmapp instance: {mtmapp}")


def setup_worker_2(wfapp: Hatchet, worker: Worker):
    @wfapp.workflow(on_events=["man:create"])
    class ManualTriggerWorkflow:
        @wfapp.step()
        def step1(self, context: Context) -> dict[str, str]:
            res = context.playground("res", "HELLO")

            # Get the directory of the current script
            script_dir = os.path.dirname(os.path.abspath(__file__))

            # Construct the path to the image file relative to the script's directory
            image_path = os.path.join(script_dir, "image.jpeg")

            # Load the image file
            with open(image_path, "rb") as image_file:
                image_data = image_file.read()

            print(len(image_data))

            # Encode the image data as base64
            base64_image = base64.b64encode(image_data).decode("utf-8")

            # Stream the base64-encoded image data
            context.put_stream(base64_image)

            time.sleep(3)
            print("executed step1")
            return {"step1": "data1 " + (res or "")}

        @wfapp.step(parents=["step1"], timeout="4s")
        def step2(self, context: Context) -> dict[str, str]:
            print("started step2")
            time.sleep(1)
            print("finished step2")
            return {"step2": "data2"}
