import asyncio

import pytest
from mtmai.hatchet import Hatchet
from mtmai.worker.worker import Worker


@pytest.mark.asyncio
async def test_workflow_boot(mtmapp: Hatchet, worker: Worker) -> None:
    """测试 worker 启动2"""
    assert mtmapp is not None
    from mtmai.flows.flow_ag import FlowAg

    worker.register_workflow(FlowAg())
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
