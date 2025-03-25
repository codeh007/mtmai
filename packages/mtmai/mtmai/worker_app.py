from loguru import logger

from mtmai.core.config import settings
from mtmai.hatchet import Hatchet

mtmapp = Hatchet()


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
    # for workflow_type in get_workflows_types():
    #     worker.register_workflow(workflow_type())

    from flows.flow_tenant import FlowTenant

    worker.register_workflow(FlowTenant())
    logger.info("register tenant workflow")

    from flows.flow_tenant_settings import FlowTenantSettings

    worker.register_workflow(FlowTenantSettings())
    logger.info("register tenant settings workflow")

    from flows.flow_smolagent import FlowSmolagent

    worker.register_workflow(FlowSmolagent())
    logger.info("register smolagent workflow")

    from flows.flow_team import FlowTeam

    worker.register_workflow(FlowTeam())
    logger.info("register team workflow")

    from flows.flow_manager import FlowManager

    worker.register_workflow(FlowManager())
    logger.info("register manager workflow")

    from flows.flow_research import FlowResearch

    worker.register_workflow(FlowResearch())
    logger.info("register research workflow")

    from flows.flow_browser import FlowBrowser

    worker.register_workflow(FlowBrowser())
    logger.info("register browser workflow")

    from flows.flow_ag import FlowAg

    worker.register_workflow(FlowAg())
    logger.info("register ag workflow")

    from flows.flow_com import FlowCom

    worker.register_workflow(FlowCom())
    logger.info("register com workflow")

    from flows.flow_ig import FlowIG

    worker.register_workflow(FlowIG())
    logger.info("register ig workflow")

    # from flows.flow_model import FlowModel

    # worker.register_workflow(FlowModel())
    # logger.info("register model workflow")

    await worker.async_start()
