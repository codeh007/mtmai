import asyncio
from typing import cast

import pytest
from mtmai.agents.worker_agent.worker_team import WorkerTeam
from mtmai.clients.agent_runtime.mtm_runtime import GrpcWorkerAgentRuntime
from mtmai.context.context import Context
from mtmai.hatchet import Hatchet
from mtmai.mtmpb.ag_pb2 import AgentRunInput
from mtmai.worker.worker import Worker


@pytest.mark.asyncio
async def test_workflow_boot(mtmapp: Hatchet, worker: Worker) -> None:
    """测试 worker 启动2"""
    assert mtmapp is not None
    await setup_example_workflows(mtmapp, worker)
    # await setup_worker_2(mtmapp, worker)
    worker_task = asyncio.create_task(worker.async_start())
    try:
        # worker 五秒内不报错,视为通过
        await asyncio.sleep(5)
        assert not worker_task.done(), "Worker stopped unexpectedly"

    except Exception as e:
        pytest.fail(f"Error occurred during worker execution: {str(e)}")

    finally:
        await worker.close()
        if not worker_task.done():
            worker_task.cancel()
            try:
                await worker_task
            except asyncio.CancelledError:
                pass


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

    worker.register_workflow(FlowAg())
    # print(f"Mtmapp instance: {mtmapp}")


# async def setup_worker_2(wfapp: Hatchet, worker: Worker):
#     @wfapp.workflow(on_events=["testing_man:create"])
#     class ManualTriggerWorkflow:
#         @wfapp.step()
#         def step1(self, context: Context) -> dict[str, str]:
#             res = context.playground("res", "HELLO")

#             # Get the directory of the current script
#             script_dir = os.path.dirname(os.path.abspath(__file__))

#             # Construct the path to the image file relative to the script's directory
#             image_path = os.path.join(script_dir, "image.jpeg")

#             # Load the image file
#             with open(image_path, "rb") as image_file:
#                 image_data = image_file.read()

#             print(len(image_data))

#             # Encode the image data as base64
#             base64_image = base64.b64encode(image_data).decode("utf-8")

#             # Stream the base64-encoded image data
#             context.put_stream(base64_image)

#             time.sleep(3)
#             print("executed step1")
#             return {"step1": "data1 " + (res or "")}

#         @wfapp.step(parents=["step1"], timeout="4s")
#         def step2(self, context: Context) -> dict[str, str]:
#             print("started step2")
#             time.sleep(1)
#             print("finished step2")
#             return {"step2": "data2"}

#     worker.register_workflow(ManualTriggerWorkflow())
