from autogen_core import try_get_known_serializers_for_type
from loguru import logger

from mtmai.agents.greeter_team import AskToGreet, Feedback, GreeterTeam, Greeting
from mtmai.core.config import settings
from mtmai.hatchet import Hatchet
from mtmai.mtmpb.events_pb2 import ChatSessionStartEvent

mtmapp = Hatchet()


async def run_worker():
    await mtmapp.boot()

    # ag_runtime = mtmapp.agent_runtime
    # ag_runtime = MtmAgentRuntime(config=mtmapp.config)

    # await ag_runtime.start()

    # await greeter_team.run("greeter_team", ag_runtime)
    # 确保 durable 函数注册发送在 mtmapp.worker()函数之前.
    # from mtmai.flows.flow_dur import my_durable_func  # noqa

    worker = mtmapp.worker(settings.WORKER_NAME)

    worker.agent_runtime.add_message_serializer(
        try_get_known_serializers_for_type(ChatSessionStartEvent)
    )
    worker.agent_runtime.add_message_serializer(
        try_get_known_serializers_for_type(AskToGreet)
    )
    worker.agent_runtime.add_message_serializer(
        try_get_known_serializers_for_type(Greeting)
    )
    worker.agent_runtime.add_message_serializer(
        try_get_known_serializers_for_type(Feedback)
    )
    _start_coroutine = worker.agent_runtime.start()
    if _start_coroutine:
        await _start_coroutine
    greeter_team = GreeterTeam()
    await greeter_team.setup(worker.agent_runtime)
    # await setup_hatchet_workflows(mtmapp, worker)
    from mtmai.flows.flow_ag import FlowAg

    worker.register_workflow(FlowAg())
    # worker.register_workflow(FlowBrowser())

    # 非阻塞启动(注意: eventloop, 如果嵌套了,可能会莫名其妙的退出)
    # self.worker.setup_loop(asyncio.new_event_loop())
    # asyncio.create_task(self.worker.async_start())
    # 阻塞启动
    await worker.async_start()


async def start_ag_teams():
    logger.info("STARTING AG TEAMS.------------------------------------------")
    pass
