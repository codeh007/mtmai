from autogen_core import try_get_known_serializers_for_type

from mtmai.agents.greeter_team import AskToGreet, Feedback, GreeterTeam, Greeting
from mtmai.core.config import settings
from mtmai.hatchet import Hatchet
from mtmai.mtmpb.events_pb2 import ChatSessionStartEvent

mtmapp = Hatchet()

serializer_types = [ChatSessionStartEvent, AskToGreet, Greeting, Feedback]


def get_workflows_types():
    from mtmai.flows.flow_ag import FlowAg

    return [FlowAg]


async def run_worker():
    await mtmapp.boot()

    # ag_runtime = mtmapp.agent_runtime
    # ag_runtime = MtmAgentRuntime(config=mtmapp.config)

    # await ag_runtime.start()

    # await greeter_team.run("greeter_team", ag_runtime)
    # 确保 durable 函数注册发送在 mtmapp.worker()函数之前.
    # from mtmai.flows.flow_dur import my_durable_func  # noqa

    worker = mtmapp.worker(settings.WORKER_NAME)
    for serializer_type in serializer_types:
        worker.agent_runtime.add_message_serializer(
            try_get_known_serializers_for_type(serializer_type)
        )
    _start_coroutine = worker.agent_runtime.start()
    if _start_coroutine:
        await _start_coroutine
    greeter_team = GreeterTeam()
    await greeter_team.setup(worker.agent_runtime)

    for workflow_type in get_workflows_types():
        worker.register_workflow(workflow_type())

    await worker.async_start()


# async def start_ag_teams():
#     logger.info("STARTING AG TEAMS.------------------------------------------")
#     pass
