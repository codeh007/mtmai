import asyncio
import json
import uuid
from typing import List, Tuple

from autogen_agentchat.base import TerminationCondition
from autogen_agentchat.messages import AgentEvent, ChatMessage
from autogen_core import (
    CancellationToken,
    ClosureAgent,
    ClosureContext,
    Component,
    DefaultSubscription,
    DefaultTopicId,
    FunctionCall,
    MessageContext,
    RoutedAgent,
    SingleThreadedAgentRuntime,
    TopicId,
    TypeSubscription,
    message_handler,
    try_get_known_serializers_for_type,
)
from autogen_core.models import (
    AssistantMessage,
    ChatCompletionClient,
    FunctionExecutionResult,
    FunctionExecutionResultMessage,
    LLMMessage,
    SystemMessage,
    UserMessage,
)
from autogen_core.tools import FunctionTool, Tool
from loguru import logger
from mtmai.context.context_client import TenantClient
from mtmai.teams.base_team import MtBaseTeam
from pydantic import BaseModel


class MyMessage(BaseModel):
    content: str


class UserLogin(BaseModel):
    pass


class UserTask(BaseModel):
    context: List[LLMMessage]


class AgentResponse(BaseModel):
    reply_to_topic_type: str
    context: List[LLMMessage]


# def percentage_change_tool(start: float, end: float) -> float:
#     return ((end - start) / start) * 100


class AIAgent(RoutedAgent):
    def __init__(
        self,
        description: str,
        system_message: SystemMessage,
        model_client: ChatCompletionClient,
        tools: List[Tool],
        delegate_tools: List[Tool],
        agent_topic_type: str,
        user_topic_type: str,
    ) -> None:
        super().__init__(description)
        self._system_message = system_message
        self._model_client = model_client
        self._tools = dict([(tool.name, tool) for tool in tools])
        self._tool_schema = [tool.schema for tool in tools]
        self._delegate_tools = dict([(tool.name, tool) for tool in delegate_tools])
        self._delegate_tool_schema = [tool.schema for tool in delegate_tools]
        self._agent_topic_type = agent_topic_type
        self._user_topic_type = user_topic_type

    @message_handler
    async def handle_task(self, message: UserTask, ctx: MessageContext) -> None:
        # Send the task to the LLM.
        llm_result = await self._model_client.create(
            messages=[self._system_message] + message.context,
            tools=self._tool_schema + self._delegate_tool_schema,
            cancellation_token=ctx.cancellation_token,
        )
        print(f"{'-'*80}\n{self.id.type}:\n{llm_result.content}", flush=True)
        # Process the LLM result.
        while isinstance(llm_result.content, list) and all(
            isinstance(m, FunctionCall) for m in llm_result.content
        ):
            tool_call_results: List[FunctionExecutionResult] = []
            delegate_targets: List[Tuple[str, UserTask]] = []
            # Process each function call.
            for call in llm_result.content:
                arguments = json.loads(call.arguments)
                if call.name in self._tools:
                    # Execute the tool directly.
                    result = await self._tools[call.name].run_json(
                        arguments, ctx.cancellation_token
                    )
                    result_as_str = self._tools[call.name].return_value_as_string(
                        result
                    )
                    tool_call_results.append(
                        FunctionExecutionResult(
                            call_id=call.id,
                            content=result_as_str,
                            is_error=False,
                            name=call.name,
                        )
                    )
                elif call.name in self._delegate_tools:
                    # Execute the tool to get the delegate agent's topic type.
                    result = await self._delegate_tools[call.name].run_json(
                        arguments, ctx.cancellation_token
                    )
                    topic_type = self._delegate_tools[call.name].return_value_as_string(
                        result
                    )
                    # Create the context for the delegate agent, including the function call and the result.
                    delegate_messages = list(message.context) + [
                        AssistantMessage(content=[call], source=self.id.type),
                        FunctionExecutionResultMessage(
                            content=[
                                FunctionExecutionResult(
                                    call_id=call.id,
                                    content=f"Transferred to {topic_type}. Adopt persona immediately.",
                                    is_error=False,
                                    name=call.name,
                                )
                            ]
                        ),
                    ]
                    delegate_targets.append(
                        (topic_type, UserTask(context=delegate_messages))
                    )
                else:
                    raise ValueError(f"Unknown tool: {call.name}")
            if len(delegate_targets) > 0:
                # Delegate the task to other agents by publishing messages to the corresponding topics.
                for topic_type, task in delegate_targets:
                    print(
                        f"{'-'*80}\n{self.id.type}:\nDelegating to {topic_type}",
                        flush=True,
                    )
                    await self.publish_message(
                        task, topic_id=TopicId(topic_type, source=self.id.key)
                    )
            if len(tool_call_results) > 0:
                print(f"{'-'*80}\n{self.id.type}:\n{tool_call_results}", flush=True)
                # Make another LLM call with the results.
                message.context.extend(
                    [
                        AssistantMessage(
                            content=llm_result.content, source=self.id.type
                        ),
                        FunctionExecutionResultMessage(content=tool_call_results),
                    ]
                )
                llm_result = await self._model_client.create(
                    messages=[self._system_message] + message.context,
                    tools=self._tool_schema + self._delegate_tool_schema,
                    cancellation_token=ctx.cancellation_token,
                )
                print(f"{'-'*80}\n{self.id.type}:\n{llm_result.content}", flush=True)
            else:
                # The task has been delegated, so we are done.
                return
        # The task has been completed, publish the final result.
        assert isinstance(llm_result.content, str)
        message.context.append(
            AssistantMessage(content=llm_result.content, source=self.id.type)
        )
        await self.publish_message(
            AgentResponse(
                context=message.context, reply_to_topic_type=self._agent_topic_type
            ),
            topic_id=TopicId(self._user_topic_type, source=self.id.key),
        )


class HumanAgent(RoutedAgent):
    def __init__(
        self, description: str, agent_topic_type: str, user_topic_type: str
    ) -> None:
        super().__init__(description)
        self._agent_topic_type = agent_topic_type
        self._user_topic_type = user_topic_type

    @message_handler
    async def handle_user_task(self, message: UserTask, ctx: MessageContext) -> None:
        human_input = input("Human agent input: ")
        print(f"{'-'*80}\n{self.id.type}:\n{human_input}", flush=True)
        message.context.append(
            AssistantMessage(content=human_input, source=self.id.type)
        )
        await self.publish_message(
            AgentResponse(
                context=message.context, reply_to_topic_type=self._agent_topic_type
            ),
            topic_id=TopicId(self._user_topic_type, source=self.id.key),
        )


class UserAgent(RoutedAgent):
    def __init__(
        self, description: str, user_topic_type: str, agent_topic_type: str
    ) -> None:
        super().__init__(description)
        self._user_topic_type = user_topic_type
        self._agent_topic_type = agent_topic_type

    @message_handler
    async def handle_user_login(self, message: UserLogin, ctx: MessageContext) -> None:
        print(f"{'-'*80}\nUser login, session ID: {self.id.key}.", flush=True)
        # Get the user's initial input after login.
        user_input = input("User: ")
        print(f"{'-'*80}\n{self.id.type}:\n{user_input}")
        await self.publish_message(
            UserTask(context=[UserMessage(content=user_input, source="User")]),
            topic_id=TopicId(self._agent_topic_type, source=self.id.key),
        )

    @message_handler
    async def handle_task_result(
        self, message: AgentResponse, ctx: MessageContext
    ) -> None:
        # Get the user's input after receiving a response from an agent.
        user_input = input("User (type 'exit' to close the session): ")
        print(f"{'-'*80}\n{self.id.type}:\n{user_input}", flush=True)
        if user_input.strip().lower() == "exit":
            print(f"{'-'*80}\nUser session ended, session ID: {self.id.key}.")
            return
        message.context.append(UserMessage(content=user_input, source="User"))
        await self.publish_message(
            UserTask(context=message.context),
            topic_id=TopicId(message.reply_to_topic_type, source=self.id.key),
        )


def execute_order(product: str, price: int) -> str:
    print("\n\n=== Order Summary ===")
    print(f"Product: {product}")
    print(f"Price: ${price}")
    print("=================\n")
    confirm = input("Confirm order? y/n: ").strip().lower()
    if confirm == "y":
        print("Order execution successful!")
        return "Success"
    else:
        print("Order cancelled!")
        return "User cancelled order."


def look_up_item(search_query: str) -> str:
    item_id = "item_132612938"
    print("Found item:", item_id)
    return item_id


def execute_refund(item_id: str, reason: str = "not provided") -> str:
    print("\n\n=== Refund Summary ===")
    print(f"Item ID: {item_id}")
    print(f"Reason: {reason}")
    print("=================\n")
    print("Refund execution successful!")
    return "success"


execute_order_tool = FunctionTool(execute_order, description="Price should be in USD.")
look_up_item_tool = FunctionTool(
    look_up_item,
    description="Use to find item ID.\nSearch query can be a description or keywords.",
)
execute_refund_tool = FunctionTool(execute_refund, description="")


sales_agent_topic_type = "SalesAgent"
issues_and_repairs_agent_topic_type = "IssuesAndRepairsAgent"
triage_agent_topic_type = "TriageAgent"
human_agent_topic_type = "HumanAgent"
user_topic_type = "User"


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


class DemoHandoffsTeam(MtBaseTeam, Component[DemoHandoffsTeamConfig]):
    component_type = "team"

    # @property
    # def name(self):
    #     return "demo_handoffs_team"

    # @property
    # def description(self):
    #     return "人机交互团队"

    def __init__(
        self,
        # participants: List[ChatAgent],
        # group_chat_manager_class: type[SequentialRoutedAgent],
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
        self._runtime = SingleThreadedAgentRuntime(ignore_unhandled_exceptions=False)

        # Flag to track if the group chat has been initialized.
        self._initialized = False

        # Flag to track if the group chat is running.
        self._is_running = False

    async def _init(self) -> None:
        # self._runtime = self._runtime
        # self._runtime = SingleThreadedAgentRuntime()

        tenant_client = TenantClient()
        tid = tenant_client.tenant_id
        model_client = await tenant_client.ag.default_model_client(tid)

        # Register the triage agent.
        triage_agent_type = await AIAgent.register(
            self._runtime,
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
            TypeSubscription(
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

        await ClosureAgent.register_closure(
            runtime=self._runtime,
            type="collector",
            closure=collect_output_messages,
            # subscriptions=lambda: [
            #     TypeSubscription(
            #         topic_type=self._output_topic_type,
            #         agent_type=self._collector_agent_type,
            #     ),
            # ],
            subscriptions=lambda: [DefaultSubscription()],
        )

        await self._runtime.add_message_serializer(
            try_get_known_serializers_for_type(MyMessage)
        )

        self._initialized = True

    async def run(self, task=None, cancellation_token: CancellationToken | None = None):
        # queue = asyncio.Queue[MyMessage]()
        if not self._initialized:
            await self._init(self._runtime)

        async def output_result(
            _ctx: ClosureContext,
            # message: MyMessage,
            message: BaseModel,
            ctx: MessageContext,
        ) -> None:
            # await queue.put(message)
            print(f"收到消息: message: {message}")

        await ClosureAgent.register_closure(
            runtime=self._runtime,
            type="closure_agent123",
            closure=output_result,
            subscriptions=lambda: [DefaultSubscription()],
        )

        self._runtime.start()
        await self._runtime.publish_message(
            MyMessage(content="Hello, world!"), DefaultTopicId()
        )
        await self._runtime.stop_when_idle()

        # result = await queue.get()

        # 阶段2
        # self._runtime.start()

        # Create a new session for the user.
        session_id = str(uuid.uuid4())
        await self._runtime.publish_message(
            UserLogin(), topic_id=TopicId(user_topic_type, source=session_id)
        )
        await self._runtime.stop_when_idle()
