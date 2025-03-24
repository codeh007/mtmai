from loguru import logger

from mtmai.core.config import settings
from mtmai.hatchet import Hatchet

mtmapp = Hatchet()


def get_workflows_types():
    from flows.flow_tenant import FlowTenant

    from mtmai.flows.flow_ag import FlowAg
    from mtmai.flows.flow_browser import FlowBrowser
    from mtmai.flows.flow_com import FlowCom
    from mtmai.flows.flow_llm import FlowModel
    from mtmai.flows.flow_manager import FlowManager
    from mtmai.flows.flow_research import FlowResearch
    from mtmai.flows.flow_smolagent import FlowSmolagent
    from mtmai.flows.flow_team import FlowTeam
    from mtmai.flows.flow_tenant_settings import FlowTenantSettings

    return [
        FlowAg,
        FlowTenantSettings,
        FlowSmolagent,
        FlowTeam,
        FlowManager,
        FlowResearch,
        FlowBrowser,
        FlowModel,
        FlowCom,
        FlowTenant,
    ]


async def run_worker():
    logger.info("booting worker")
    await mtmapp.boot()
    # await greeter_team.run("greeter_team", ag_runtime)
    # 确保 durable 函数注册发送在 mtmapp.worker()函数之前.
    # from mtmai.flows.flow_dur import my_durable_func  # noqa

    worker = mtmapp.worker(settings.WORKER_NAME)
    # for serializer_type in serializer_types:
    #     worker.agent_runtime.add_message_serializer(
    #         try_get_known_serializers_for_type(serializer_type)
    #     )
    _start_coroutine = worker.agent_runtime.start()
    if _start_coroutine:
        await _start_coroutine
    # greeter_team = GreeterTeam()
    # await greeter_team.setup(worker.agent_runtime)

    # 另外一个持续运行的团队
    # team2 = DemoHandoffsTeam()
    # 注册工作流
    for workflow_type in get_workflows_types():
        worker.register_workflow(workflow_type())

    await worker.async_start()
