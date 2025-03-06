import asyncio
import uuid
from typing import Any, Mapping

from autogen_agentchat.base import TerminationCondition
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_core import (
    AgentRuntime,
    CancellationToken,
    ClosureContext,
    Component,
    MessageContext,
    SingleThreadedAgentRuntime,
    TopicId,
    TypeSubscription,
    try_get_known_serializers_for_type,
)
from autogen_core.models import SystemMessage, UserMessage
from autogen_core.tools import FunctionTool
from loguru import logger
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx
from mtmai.mtmpb.ag_pb2 import AgentRunInput
from mtmai.teams.base_team import MtBaseTeam
from mtmai.teams.sys_team._agents import AIAgent, Hello2Agent, HumanAgent, UserAgent
from mtmai.teams.sys_team._types import (
    AgentResponse,
    Hello2Message,
    MyMessage,
    UserLogin,
    UserTask,
)
from pydantic import BaseModel

sales_agent_topic_type = "SalesAgent"
issues_and_repairs_agent_topic_type = "IssuesAndRepairsAgent"
triage_agent_topic_type = "TriageAgent"
human_agent_topic_type = "HumanAgent"
user_topic_type = "User"
hello2_topic_type = "Hello2"


def execute_order(product: str, price: int) -> str:
    logger.info("\n\n=== Order Summary ===")
    logger.info(f"Product: {product}")
    logger.info(f"Price: ${price}")
    logger.info("=================\n")
    confirm = input("Confirm order? y/n: ").strip().lower()
    if confirm == "y":
        logger.info("Order execution successful!")
        return "Success"
    else:
        logger.info("Order cancelled!")
        return "User cancelled order."


def look_up_item(search_query: str) -> str:
    item_id = "item_132612938"
    logger.info("Found item:", item_id)
    return item_id


def execute_refund(item_id: str, reason: str = "not provided") -> str:
    logger.info("\n\n=== Refund Summary ===")
    logger.info(f"Item ID: {item_id}")
    logger.info(f"Reason: {reason}")
    logger.info("=================\n")
    logger.info("Refund execution successful!")
    return "success"


execute_order_tool = FunctionTool(execute_order, description="Price should be in USD.")
look_up_item_tool = FunctionTool(
    look_up_item,
    description="Use to find item ID.\nSearch query can be a description or keywords.",
)
execute_refund_tool = FunctionTool(execute_refund, description="")


def transfer_to_sales_agent() -> str:
    return sales_agent_topic_type


def transfer_to_issues_and_repairs() -> str:
    return issues_and_repairs_agent_topic_type


def transfer_back_to_triage() -> str:
    return triage_agent_topic_type


def escalate_to_human() -> str:
    return human_agent_topic_type


# Delegate tools for the AI agents
transfer_to_sales_agent_tool = FunctionTool(
    transfer_to_sales_agent, description="Use for anything sales or buying related."
)
transfer_to_issues_and_repairs_tool = FunctionTool(
    transfer_to_issues_and_repairs, description="Use for issues, repairs, or refunds."
)
transfer_back_to_triage_tool = FunctionTool(
    transfer_back_to_triage,
    description="Call this if the user brings up a topic outside of your purview,\nincluding escalating to human.",
)
escalate_to_human_tool = FunctionTool(
    escalate_to_human, description="Only call this if explicitly asked to."
)


class DemoHandoffsTeamConfig(BaseModel):
    # participants: List[ComponentModel]
    # termination_condition: ComponentModel | None = None
    # max_turns: int | None = None
    ...


# Closure
async def collect_output_messages(
    _runtime: ClosureContext,
    message: UserLogin,
    ctx: MessageContext,
) -> None:
    """Collect output messages from the group chat."""
    # if isinstance(message, GroupChatStart):
    #     if message.messages is not None:
    #         for msg in message.messages:
    #             event_logger.info(msg)
    #             await self._output_message_queue.put(msg)
    # elif isinstance(message, GroupChatMessage):
    #     event_logger.info(message.message)
    #     await self._output_message_queue.put(message.message)
    # elif isinstance(message, GroupChatTermination):
    #     event_logger.info(message.message)
    #     self._stop_reason = message.message.content
    logger.info(f"收到消息: message: {message}")


class DemoHandoffsTeam(MtBaseTeam, Component[DemoHandoffsTeamConfig]):
    component_type = "team"

    def __init__(
        self,
        termination_condition: TerminationCondition | None = None,
        max_turns: int | None = None,
    ) -> None:
        self._termination_condition = termination_condition
        self._max_turns = max_turns

        # Constants for the group chat.
        self._team_id = str(uuid.uuid4())
        self._group_topic_type = "group_topic"
        self._output_topic_type = "output_topic"
        self._group_chat_manager_topic_type = "group_chat_manager"
        # self._participant_topic_types: List[str] = [
        #     participant.name for participant in participants
        # ]
        # self._participant_descriptions: List[str] = [
        #     participant.description for participant in participants
        # ]
        self._collector_agent_type = "collect_output_messages"

        # Constants for the closure agent to collect the output messages.
        self._stop_reason: str | None = None
        self._output_message_queue: asyncio.Queue[AgentEvent | ChatMessage | None] = (
            asyncio.Queue()
        )

        # Create a runtime for the team.
        # TODO: The runtime should be created by a managed context.
        # Background exceptions must not be ignored as it results in non-surfaced exceptions and early team termination.
        self._runtime = SingleThreadedAgentRuntime(
            # ignore_unhandled_exceptions=False,
        )
        self._initialized = False
        self._is_running = False

    async def _init(self, runtime: AgentRuntime | None = None) -> None:
        tenant_client = TenantClient()
        tid = tenant_client.tenant_id
        model_client = await tenant_client.ag.default_model_client(tid)

        # Register the triage agent.
        triage_agent_type = await AIAgent.register(
            runtime=self._runtime,
            type=triage_agent_topic_type,  # Using the topic type as the agent type.
            factory=lambda: AIAgent(
                description="A triage agent.",
                system_message=SystemMessage(
                    content="You are a customer service bot for ACME Inc. "
                    "Introduce yourself. Always be very brief. "
                    "Gather information to direct the customer to the right department. "
                    "But make your questions subtle and natural."
                ),
                model_client=model_client,
                tools=[],
                delegate_tools=[
                    transfer_to_issues_and_repairs_tool,
                    transfer_to_sales_agent_tool,
                    escalate_to_human_tool,
                ],
                agent_topic_type=triage_agent_topic_type,
                user_topic_type=user_topic_type,
            ),
        )
        # Add subscriptions for the triage agent: it will receive messages published to its own topic only.
        await self._runtime.add_subscription(
            subscription=TypeSubscription(
                topic_type=triage_agent_topic_type, agent_type=triage_agent_type.type
            )
        )

        # Register the sales agent.
        sales_agent_type = await AIAgent.register(
            self._runtime,
            type=sales_agent_topic_type,  # Using the topic type as the agent type.
            factory=lambda: AIAgent(
                description="A sales agent.",
                system_message=SystemMessage(
                    content="You are a sales agent for ACME Inc."
                    "Always answer in a sentence or less."
                    "Follow the following routine with the user:"
                    "1. Ask them about any problems in their life related to catching roadrunners.\n"
                    "2. Casually mention one of ACME's crazy made-up products can help.\n"
                    " - Don't mention price.\n"
                    "3. Once the user is bought in, drop a ridiculous price.\n"
                    "4. Only after everything, and if the user says yes, "
                    "tell them a crazy caveat and execute their order.\n"
                    ""
                ),
                model_client=model_client,
                tools=[execute_order_tool],
                delegate_tools=[transfer_back_to_triage_tool],
                agent_topic_type=sales_agent_topic_type,
                user_topic_type=user_topic_type,
            ),
        )
        # Add subscriptions for the sales agent: it will receive messages published to its own topic only.
        await self._runtime.add_subscription(
            TypeSubscription(
                topic_type=sales_agent_topic_type, agent_type=sales_agent_type.type
            )
        )

        # Register the issues and repairs agent.
        issues_and_repairs_agent_type = await AIAgent.register(
            self._runtime,
            type=issues_and_repairs_agent_topic_type,  # Using the topic type as the agent type.
            factory=lambda: AIAgent(
                description="An issues and repairs agent.",
                system_message=SystemMessage(
                    content="You are a customer support agent for ACME Inc."
                    "Always answer in a sentence or less."
                    "Follow the following routine with the user:"
                    "1. First, ask probing questions and understand the user's problem deeper.\n"
                    " - unless the user has already provided a reason.\n"
                    "2. Propose a fix (make one up).\n"
                    "3. ONLY if not satisfied, offer a refund.\n"
                    "4. If accepted, search for the ID and then execute refund."
                ),
                model_client=model_client,
                tools=[
                    execute_refund_tool,
                    look_up_item_tool,
                ],
                delegate_tools=[transfer_back_to_triage_tool],
                agent_topic_type=issues_and_repairs_agent_topic_type,
                user_topic_type=user_topic_type,
            ),
        )
        # Add subscriptions for the issues and repairs agent: it will receive messages published to its own topic only.
        await self._runtime.add_subscription(
            TypeSubscription(
                topic_type=issues_and_repairs_agent_topic_type,
                agent_type=issues_and_repairs_agent_type.type,
            )
        )

        # Register the human agent.
        human_agent_type = await HumanAgent.register(
            self._runtime,
            type=human_agent_topic_type,  # Using the topic type as the agent type.
            factory=lambda: HumanAgent(
                description="A human agent.",
                agent_topic_type=human_agent_topic_type,
                user_topic_type=user_topic_type,
            ),
        )
        # Add subscriptions for the human agent: it will receive messages published to its own topic only.
        await self._runtime.add_subscription(
            TypeSubscription(
                topic_type=human_agent_topic_type, agent_type=human_agent_type.type
            )
        )

        # Register the user agent.
        user_agent_type = await UserAgent.register(
            self._runtime,
            type=user_topic_type,
            factory=lambda: UserAgent(
                description="A user agent.",
                user_topic_type=user_topic_type,
                agent_topic_type=triage_agent_topic_type,  # Start with the triage agent.
            ),
        )
        # Add subscriptions for the user agent: it will receive messages published to its own topic only.
        await self._runtime.add_subscription(
            TypeSubscription(
                topic_type=user_topic_type, agent_type=user_agent_type.type
            )
        )

        hello2_agent_type = await Hello2Agent.register(
            runtime=self._runtime,
            type=hello2_topic_type,
            factory=lambda: Hello2Agent(
                description="A hello2 agent.",
            ),
        )
        await self._runtime.add_subscription(
            TypeSubscription(
                topic_type=hello2_topic_type, agent_type=hello2_agent_type.type
            )
        )

        # await ClosureAgent.register_closure(
        #     runtime=self._runtime,
        #     type="collector",
        #     closure=collect_output_messages,
        #     # subscriptions=lambda: [
        #     #     TypeSubscription(
        #     #         topic_type=self._output_topic_type,
        #     #         agent_type=self._collector_agent_type,
        #     #     ),
        #     # ],
        #     subscriptions=lambda: [DefaultSubscription()],
        # )

        self._runtime.add_message_serializer(
            try_get_known_serializers_for_type(MyMessage)
        )
        self._runtime.add_message_serializer(
            try_get_known_serializers_for_type(Hello2Message)
        )
        self._runtime.add_message_serializer(
            try_get_known_serializers_for_type(UserLogin)
        )
        self._runtime.add_message_serializer(
            try_get_known_serializers_for_type(UserTask)
        )
        self._runtime.add_message_serializer(
            try_get_known_serializers_for_type(AgentResponse)
        )

        self._initialized = True
        self._runtime.start()

    async def run(
        self,
        task=AgentRunInput,
        cancellation_token: CancellationToken | None = None,
    ):
        if cancellation_token and cancellation_token.is_cancelled():
            logger.info("cancellation_token is cancelled")
            return
        if not self._initialized:
            await self._init(self._runtime)

        session_id = get_chat_session_id_ctx()

        user_content = task.content
        if user_content == "/test_login":
            await self._runtime.publish_message(
                message=UserLogin(),
                topic_id=TopicId(user_topic_type, source=session_id),
            )
        elif user_content.startswith("/hello2"):
            await self._runtime.publish_message(
                message=Hello2Message(),
                topic_id=TopicId(hello2_topic_type, source=session_id),
            )
        elif user_content.startswith("/user_content"):
            # await self._runtime.publish_message(
            #     message=UserTask(
            #         context=[UserMessage(content="user_content123", source="User")]
            #     ),
            #     topic_id=TopicId(triage_agent_topic_type, source=session_id),
            # )
            await self._runtime.publish_message(
                message=UserTask(
                    context=[UserMessage(content="user_content123", source="User")]
                ),
                topic_id=TopicId(triage_agent_topic_type, source=session_id),
            )

        else:
            raise ValueError(f"Invalid user content: {user_content}")

        # TODO: 对于系统团队的停止方式,应该在 worker 中实现,这个团队应该跟随worker的停止而停止
        # await self._runtime.stop_when_idle()

    async def save_state(self) -> Mapping[str, Any]:
        """保存团队状态
        提示1: 不必等到 runtime 停止.
        """
        # if not self._initialized:
        #     raise RuntimeError(
        #         "The group chat has not been initialized. It must be run before it can be saved."
        #     )

        # if self._is_running:
        #     raise RuntimeError("The team cannot be saved while it is running.")
        # self._is_running = True

        # try:
        #     # Save the state of the runtime. This will save the state of the participants and the group chat manager.
        #     agent_states = await self._runtime.save_state()
        #     return TeamState(
        #         agent_states=agent_states, team_id=self._team_id
        #     ).model_dump()
        # finally:
        #     # Indicate that the team is no longer running.
        #     self._is_running = False
        pass

    async def load_state(self, state: Mapping[str, Any]) -> None:
        # """Load the state of the group chat team."""
        # if not self._initialized:
        #     await self._init(self._runtime)

        # if self._is_running:
        #     raise RuntimeError("The team cannot be loaded while it is running.")
        # self._is_running = True

        # try:
        #     # Load the state of the runtime. This will load the state of the participants and the group chat manager.
        #     team_state = TeamState.model_validate(state)
        #     self._team_id = team_state.team_id
        #     await self._runtime.load_state(team_state.agent_states)
        # finally:
        #     # Indicate that the team is no longer running.
        #     self._is_running = False

        pass

    async def show_state(self) -> None:
        pass
