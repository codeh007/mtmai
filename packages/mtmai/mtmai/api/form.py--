import json
from typing import Any, Type
from camelCasing import camelCasing
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
import structlog
from mtmai.db.db import get_async_session
from mtmai.deps import AsyncSessionDep, CurrentUser
from mtmai.flows.site_flows import FlowBase, create_site_task
from mtmai.models.site import Site
from mtmlib.decorators.mtform.mtform import FormFieldSchema, MtForm

LOG = structlog.get_logger()

router = APIRouter()


class OpenFormRequest(BaseModel):
    formName: str


class SchemaFormRequest(BaseModel):
    formName: str


@router.get("/schema_form/{name}", response_model=MtForm)
async def schema_form(name: str):
    name = camelCasing.toCamelCase(name)
    names = [name, name + "Form", name + "Request"]

    form_class: Type[BaseModel] = None
    for flow_class in FlowBase.__subclasses__():
        if hasattr(flow_class, "form_model"):
            form_name = flow_class.form_model.__name__
            if form_name in names or camelCasing.toCamelCase(form_name) in names:
                form_class = flow_class.form_model
                break

    if form_class is None:
        raise HTTPException(status_code=404, detail=f"Form '{name}' not found")

    schema = form_class.model_json_schema()
    properties = schema.get("properties", {})

    mtform_properties = {}
    for k, v in properties.items():
        field_schema = FormFieldSchema(
            name=k,
            placeholder=v.get("placeholder"),
            valueType=v.get("type"),
            defaultValue=v.get("default"),
            description=v.get("description"),
            label=v.get("title"),
            type=v.get("format") or v.get("type"),
        )
        mtform_properties[k] = field_schema

    mtform_instance = MtForm(
        properties=mtform_properties,
        title=schema.get("title", ""),
        type=schema.get("type", "object"),
        variant="default",
    )

    return mtform_instance


class SubmitSchemaFormRequest(BaseModel):
    form_name: str
    form_data: dict


class SubmitSchemaFormResponse(BaseModel):
    flow_run_id: str
    flow_run_status: str | None = None
    flow_run_message: str | None = None
    flow_run_result: Any | None = None


@router.post("/submit_schema_form")
async def submit_schema_form(
    req: Request,
    session: AsyncSessionDep,
    current_user: CurrentUser,
):
    """接受动态表单提交，触发工作流运行，并流式回传 http stream 事件"""
    request_data = await req.json()
    messages = request_data.get("messages")
    if not messages or len(messages) == 0:
        raise HTTPException(status_code=400, detail="No messages provided")
    latest_message = messages[-1]
    formReq = SubmitSchemaFormRequest(**json.loads(latest_message.get("content")))

    form_name = camelCasing.toCamelCase(formReq.form_name)
    flow_class = next(
        (
            cls
            for cls in FlowBase.__subclasses__()
            if cls.form_model.__name__ == form_name
            or camelCasing.toCamelCase(cls.form_model.__name__) == form_name
            or camelCasing.toCamelCase(cls.form_model.__name__) == form_name + "Form"
            or camelCasing.toCamelCase(cls.form_model.__name__) == form_name + "Request"
        ),
        None,
    )
    if not flow_class:
        raise HTTPException(
            status_code=404, detail=f"Flow for form {formReq.form_name} not found"
        )

    try:
        # # 实验：为每个站点单独建立一个部署
        # from prefect.deployments import Deployment
        # from prefect.server.schemas.schedules import CronSchedule

        # from prefect.deployments import run_deployment

        # deployment = Deployment.build_from_flow(
        #     flow=manage_all_sites,
        #     name="manage_all_sites_deployment",
        #     schedule=CronSchedule(cron="0 * * * *"),  # 每小时运行一次
        # )
        # deployment.apply()

        from prefect.events import emit_event

        async with get_async_session() as session:
            new_site = Site.model_validate(
                formReq.form_data, update={"owner_id": str(current_user.id)}
            )
            session.add(new_site)
            await session.commit()
            await session.refresh(new_site)

            await create_site_task(session, new_site.id, current_user.id)
        event = emit_event(
            event="mtmai.site.create",
            resource={
                "prefect.resource.id": "my.external.resource",
                "user_id": str(current_user.id),
                "site_id": str(new_site.id),
            },
        )
        LOG.info(event)

        # async with get_client() as client:
        #     deployments = await client.read_deployments()
        #     print(deployments)
        # async with get_client() as client:
        # from prefect.deployments import run_deployment
        # from prefect.states import Running

        # flow_run = await client.create_flow_run(
        #     flow=create_site_flow2,
        #     parameters={"data": formReq.form_data, "user_id": str(current_user.id)},
        # )
        # await client.set_flow_run_state(flow_run_id=flow_run.id, state=Running())

        # flow_run = await run_deployment(
        #     name="CreateSiteFlow2/create_site_flow2",  # 替换为您的实际部署名称
        #     parameters={"data": formReq.form_data, "user_id": str(current_user.id)},
        #     client=client,
        # )
        # ret = SubmitSchemaFormResponse(
        #     flow_run_id=str(flow_run.id),
        # )
        return {"ok": True}
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"error: {str(e)}")


@router.get("/workflow_status/{flow_run_id}")
async def get_workflow_status(flow_run_id: str):
    """获取工作流的实时状态"""
    from prefect import get_client

    async with get_client() as client:
        try:
            flow_run = await client.read_flow_run(flow_run_id)
            return {
                "status": flow_run.state.type.value,
                "message": flow_run.state.message,
                "result": flow_run.state.result()
                if flow_run.state.is_completed()
                else None,
            }
        except Exception as e:
            raise HTTPException(status_code=404, detail=f"Flow run not found: {str(e)}")
