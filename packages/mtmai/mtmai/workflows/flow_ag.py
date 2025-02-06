import logging
from typing import cast

from agents.ctx import AgentContext
from autogen_agentchat.base import TaskResult
from autogen_agentchat.messages import TextMessage
from mtmaisdk.clients.rest.models import PostizState
from mtmaisdk.clients.rest.models.ag_event_create import AgEventCreate
from mtmaisdk.context.context import Context
from pydantic import BaseModel

from mtmai.ag.team_builder import TeamBuilder
from mtmai.agents.ctx import get_mtmai_context, init_mtmai_context
from mtmai.worker import wfapp

logger = logging.getLogger(__name__)


async def run_stream(task: str):
    team_builder = TeamBuilder()
    agent = await team_builder.create_demo_agent_stream1()
    # team_runner = TeamRunner()

    # async for event in team_runner.run_stream(
    async for event in agent.run_stream(
        task=task,
        # team_config=agent.dump_component()
    ):
        if isinstance(event, TextMessage):
            yield event.model_dump()
        # elif isinstance(event, ToolCallRequestEvent):
        #     yield f"0:{json.dumps(obj=jsonable_encoder(event.content))}\n"
        # elif isinstance(event, TeamResult):
        #     yield f"0:{json.dumps(obj=event.model_dump_json())}\n"

        elif isinstance(event, BaseModel):
            # yield f"2:{event.model_dump_json()}\n"
            yield event.model_dump()
        elif isinstance(event, TaskResult):
            # 最终的结果
            # yield event
            pass
        else:
            # yield f"2:{json.dumps(f'unknown event: {str(event)},type:{type(event)}')}\n"
            yield event.model_dump()


@wfapp.workflow(
    name="ag",
    on_events=["autogen-demo:run"],
    # input_validator=PostizState,
)
class FlowAg:
    @wfapp.step(
        timeout="30m",
        # retries=1
    )
    async def step_entry(self, hatctx: Context):
        init_mtmai_context(hatctx)

        ctx: AgentContext = get_mtmai_context()
        ctx.log("FlowAg 启动")

        input: PostizState = cast(PostizState, hatctx.workflow_input())
        # hatctx.log(input)
        # ctx.log("输入: %s", input)
        # outoput = await assisant_graph.AssistantGraph.run(input)

        tenant_id = getTenantId(hatctx)
        if not tenant_id:
            raise Exception("tenantId 不能为空")
        user_id = getUserId(hatctx)
        if not user_id:
            raise Exception("userId 不能为空")
        logger.info("当前租户: %s, 当前用户: %s", tenant_id, user_id)
        # 临时代码
        r = await hatctx.rest_client.aio.ag_events_api.ag_event_list(tenant=tenant_id)
        hatctx.log(r)

        # 获取模型配置
        # user_messages = r.messages
        # if len(user_messages) == 0:
        #     raise HTTPException(status_code=400, detail="No messages provided")
        # task = user_messages[-1].content
        task = "hello"
        async for event in run_stream(task):
            hatctx.log(event)
            result = await hatctx.rest_client.aio.ag_events_api.ag_event_create(
                tenant=tenant_id,
                ag_event_create=AgEventCreate(
                    # metadata=APIResourceMeta(
                    #     id=str(uuid.uuid4()),
                    #     created_at=datetime.now(timezone.utc).isoformat(),
                    #     updated_at=datetime.now(timezone.utc).isoformat(),
                    # ),
                    user_id=user_id,
                    data=event,
                    framework="autogen",
                    stepRunId=hatctx.step_run_id,
                    meta={},
                ),
            )
            hatctx.log(result)
        return {"result": "success"}

    @wfapp.step(timeout="1m", retries=1, parents=["step_entry"])
    async def step_b(self, hatctx: Context):
        hatctx.log("stepB")
        hatctx.done()
        return {"result": "success"}

    @wfapp.step(timeout="1m", retries=1, parents=["step_b"])
    async def step_b_2(self, hatctx: Context):
        hatctx.log("stepB2")
        raise Exception("stepB2 error")

    @wfapp.step(timeout="1m", retries=1, parents=["step_b_2"])
    async def step_b_3(self, hatctx: Context):
        hatctx.log("stepB3")
        raise Exception("stepB3 error")

    @wfapp.step(timeout="1m", retries=1, parents=["step_entry"])
    async def step_c(self, hatctx: Context):
        hatctx.log("stepC")
        return {"result": "success"}


def getTenantId(hatctx: Context):
    return hatctx.additional_metadata().get("tenantId")


def getUserId(hatctx: Context):
    return hatctx.additional_metadata().get("userId")
