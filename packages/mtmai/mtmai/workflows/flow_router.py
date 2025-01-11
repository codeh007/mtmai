from typing import cast

from crewai import LLM
from mtmai.agents.ctx import init_mtmai_context
from mtmai.worker import wfapp
from mtmai.workflows.flow_crewai import FlowCrewAIAgent
from mtmai.workflows.flow_recovery import FlowRecovery
from mtmaisdk.clients.rest.models import AgentNodeRunRequest, CrewAIParams
from mtmaisdk.clients.rest.models.call_agent_llm import CallAgentLlm
from mtmaisdk.context.context import Context


@wfapp.workflow(
    on_events=["router:run"],
    input_validator=AgentNodeRunRequest,
)
class FlowRouter:
    """
    FlowRouter 调用子工作流(路由入口)

    参数应该通过工作流参数传入，原因如下：
    符合工作流设计原则
    工作流应该是自包含和确定性的
    输入参数应该完整定义工作流的执行环境
    减少额外的网络调用
    降低工作流执行的不确定性, 便于工作流的重试和重放

    快速测试:
    {
        "flow_name": "crewai",
        "isStream": false,
        "params": {}
    }
    """

    counter: int = 0

    @wfapp.step(timeout="10m", retries=1)
    async def entry(self, hatctx: Context):
        hatctx.log(f"counter: {self.counter}")
        init_mtmai_context(hatctx)
        input = cast(AgentNodeRunRequest, hatctx.workflow_input())
        hatctx.log(f"input: {input}")

        if input.flow_name == "crewai":
            params = CrewAIParams()
            hatctx.log("调用子工作流")
            try:
                await hatctx.aio.spawn_workflow(
                    FlowCrewAIAgent.__name__, params.model_dump()
                )
            except Exception as e:
                # Spawn a recovery workflow
                await hatctx.aio.spawn_workflow(
                    FlowRecovery.__name__, {"error": str(e)}
                )
            return {"next": "step_a1"}
        elif input.flow_name == "scrape":
            return {"next": "step_b1"}
        # return await StepCallAgent(hatctx).run()
        return {
            "output": "call_agent unknown flow",
        }

    async def step_agentcall_finnal(self):
        return {"output": "some thing"}

    @wfapp.step(timeout="5m")
    async def post_process(self, result: dict):
        # 后处理逻辑
        return {
            "status": "post_process",
        }

    @wfapp.step(timeout="5m", parents=["entry"])
    def step_a1(self, ctx: Context):
        # 后处理逻辑
        return {
            "output": "step_a1 result",
        }

    @wfapp.step(timeout="5m", parents=["step_a1"])
    def step_a2(self, ctx: Context):
        # 后处理逻辑
        return {
            "output": "step_a2 result",
        }

    @wfapp.step(timeout="5m", parents=["step_a2"])
    def step_a3(self, ctx: Context):
        # 后处理逻辑
        return {
            "output": "step_a3 result",
        }

    @wfapp.step(timeout="5m", parents=["entry"])
    def step_b1(self, ctx: Context):
        # 后处理逻辑
        return {
            "output": "stepb1 result",
        }

    @wfapp.step(timeout="5m", parents=["step_b1"])
    def step_b2(self, ctx: Context):
        # 后处理逻辑
        return {
            "output": "stepb2 result",
        }


def get_llm(llm_config: CallAgentLlm, callback):
    return LLM(
        model=llm_config.model,
        temperature=llm_config.temperature,
        base_url=llm_config.base_url,
        api_key=llm_config.api_key,
        num_retries=llm_config.num_retries or 3,
        logger_fn=callback,
    )
