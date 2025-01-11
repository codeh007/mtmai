import threading

import structlog

from mtmai.flows.site_flows import flow_site_automation

LOG = structlog.stdlib.get_logger()


def start_prefect_deployment(asThreading: bool = False):
    """
    部署工作流到 prefect server
    """
    # from prefect.variables import Variable

    def start_worker():
        from prefect import serve

        # 设置变量(仅作为练习)
        # Variable.set("crew_members", ["Zaphod", "Arthur", "Trillian"], overwrite=True)

        all_deployments = get_prefect_deployments()
        LOG.info(f"start prefect server, deployments: {len(all_deployments)}")
        serve(
            *all_deployments,
            limit=50,  # 默认值5
        )

    if asThreading:
        threading.Thread(target=start_worker).start()
        # start_worker()
    else:
        start_worker()


def get_prefect_deployments():
    """
    获取所有需要部署的工作流
    """
    #
    # from prefect.automations import Automation
    from prefect.events import DeploymentEventTrigger

    # from prefect.events.actions import CancelFlowRun
    # from prefect.events.schemas.automations import EventTrigger
    # from mtmai.flows.hello_flow import flow_hello
    from mtmai.flows.site_flows import (
        create_site_flow,
        flow_run_gen_article,
        flow_run_task,
    )

    # example
    # automation = Automation(
    #     name="woodchonk",
    #     trigger=EventTrigger(
    #         expect={"animal.walked"},
    #         match={
    #             "genus": "Marmota",
    #             "species": "monax",
    #         },
    #         posture="Reactive",
    #         threshold=3,
    #     ),
    #     actions=[CancelFlowRun()],
    # ).create()

    return [
        flow_site_automation.to_deployment(
            name="flow_site_automation",
            description="全部站点自动化",
            # interval=60,  # 秒
        ),
        create_site_flow.to_deployment(
            name="deployment_site_flow",
            triggers=[
                DeploymentEventTrigger(
                    enabled=True,
                    # expect=["mtmai.site.create"],
                    match={"prefect.resource.id": "my.external.resource"},
                    parameters={
                        "user_id": "{{event.resource.user_id}}",
                        "site_id": "{{event.resource.site_id}}",
                    },
                )
            ],
        ),
        # flow_hello.to_deployment(name="deployment_flow_hello"),
        flow_run_gen_article.to_deployment(
            name="deployment_flow_site_gen",
            description="单个站点自动化，将所有全托管的站点进行文章生成",
        ),
        flow_run_task.to_deployment(
            name="flow_run_task",
            description="运行单个mttask任务",
            triggers=[
                DeploymentEventTrigger(
                    enabled=True,
                    expect=["mtmai.mttask.update_status"],
                    # match={"prefect.resource.id": "my.external.resource"},
                    parameters={
                        "mttask_id": "{{event.resource.id}}",
                        # "status": "{{event.resource.status}}",
                    },
                    description="当用户主动点击任务状态按钮，触发 flow_run_task 工作流",
                )
            ],
        ),
    ]
