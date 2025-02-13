from contextlib import asynccontextmanager

from prefect import get_run_logger

from mtmai.crud.curd_logs import LogItemCreateReq, create_log_item

log_type = "mtflow"


def get_flow_util():
    return FlowsUtil()


class FlowsUtil:
    def __init__(self):
        self.logger = get_run_logger()

    async def info(self, text: str):
        self.logger.info(text)
        await create_log_item(
            LogItemCreateReq(app=log_type, text=text, type=text, level=3)
        )

    async def error(self, text: str):
        self.logger.error(text)
        await create_log_item(
            LogItemCreateReq(app=log_type, text=text, type=text, level=1)
        )

    async def warn(self, text: str):
        self.logger.warning(text)
        await create_log_item(
            LogItemCreateReq(app=log_type, text=text, type=text, level=2)
        )


@asynccontextmanager
async def mtflow_util():
    # task_id = "demo_task_id123"
    flow_util = FlowsUtil()

    # mq = MtTaskMQ(task_id)
    # await mq.init()
    await flow_util.info("任务开始-----------------------------")
    try:
        yield flow_util
    finally:
        await flow_util.info("任务完成-----------------------------")
