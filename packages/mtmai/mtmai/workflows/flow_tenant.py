import logging
import sre_compile
from typing import cast

from mtmai.ag.agents.tenant_agent import TenantAgent
from mtmaisdk.clients.rest.models.tenant_seed_req import TenantSeedReq
from agents.ctx import AgentContext
from mtmaisdk.clients.rest.models.agent_run_input import AgentRunInput
from mtmaisdk.clients.rest.models.team import Team
from mtmaisdk.clients.rest.models.team_component import TeamComponent
from mtmaisdk.context.context import Context

from mtmai.ag.team_builder.company_research import CompanyResearchTeamBuilder
from mtmai.agents.ctx import get_mtmai_context, init_mtmai_context
from mtmai.worker import wfapp
from autogen_core import AgentId, SingleThreadedAgentRuntime, TypeSubscription
from autogen_core import TopicId
from autogen_core import RoutedAgent, message_handler, type_subscription
from autogen_agentchat.messages import TextMessage

logger = logging.getLogger(__name__)


@wfapp.workflow(
    name="tenant",
    on_events=["tenant:run"],
    input_validator=TenantSeedReq,
)
class FlowTenant:
    """
    租户工作流
    """

    @wfapp.step(
        timeout="30m",
        # retries=1
    )
    async def step_reset_tenant(self, hatctx: Context):
        init_mtmai_context(hatctx)
        ctx: AgentContext = get_mtmai_context()
        ctx.set_hatch_context(hatctx)
        # 新版功能
        runtime = SingleThreadedAgentRuntime()
        await TenantAgent.register(runtime, "tenant_agent", lambda: TenantAgent(ctx))
        # await runtime.add_subscription(TypeSubscription(topic_type="tenant", agent_type="broadcasting_agent"))

        runtime.start()  # Start processing messages in the background.
        # await runtime.send_message(
        #     message=input,
        #     recipient=AgentId(type="tenant_agent", key="default"),
        # )
        # 广播方从而避免工作流中消息类型的相关转换问题.
        await runtime.publish_message(
            TextMessage(source="workflow", content="Hello, World! From the runtime!"),
            topic_id=TopicId(type="tenant", source="tenant"),
        )

        await runtime.stop_when_idle()  # This will block until the runtime is idle.
        await runtime.close()
        return {"result": "success"}

