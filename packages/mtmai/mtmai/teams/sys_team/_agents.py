import json
from typing import List, Tuple

from autogen_core import (
    FunctionCall,
    MessageContext,
    RoutedAgent,
    TopicId,
    message_handler,
)
from autogen_core.models import (
    AssistantMessage,
    ChatCompletionClient,
    FunctionExecutionResult,
    FunctionExecutionResultMessage,
    SystemMessage,
    UserMessage,
)
from autogen_core.tools import Tool
from loguru import logger
from mtmai.teams.sys_team._types import (
    AgentResponse,
    Hello2Message,
    UserLogin,
    UserTask,
)


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
        # print(f"{'-'*80}\n{self.id.type}:\n{llm_result.content}", flush=True)
        logger.info(f"{'-'*80}\n{self.id.type}:\n{llm_result.content}")
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
                # print(f"{'-'*80}\n{self.id.type}:\n{llm_result.content}", flush=True)
                logger.info(f"{'-'*80}\n{self.id.type}:\n{llm_result.content}")
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
        logger.info(f"{'-'*80}\n{self.id.type}:\n{human_input}", flush=True)
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
        # self._user_topic_type = user_topic_type
        self._agent_topic_type = agent_topic_type

    @message_handler
    async def handle_user_login(self, message: UserLogin, ctx: MessageContext) -> None:
        logger.info(f"{'-'*80}\nUser login, session ID: {self.id.key}.", flush=True)
        # Get the user's initial input after login.
        user_input = input("User: ")
        logger.info(f"{'-'*80}\n{self.id.type}:\n{user_input}")
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
        logger.info(f"{'-'*80}\n{self.id.type}:\n{user_input}")
        if user_input.strip().lower() == "exit":
            logger.info(f"{'-'*80}\nUser session ended, session ID: {self.id.key}.")
            return
        message.context.append(UserMessage(content=user_input, source="User"))
        await self.publish_message(
            UserTask(context=message.context),
            topic_id=TopicId(message.reply_to_topic_type, source=self.id.key),
        )


class Hello2Agent(RoutedAgent):
    def __init__(self, description: str) -> None:
        super().__init__(description)
        # 不需要这些注释掉的代码
        # self._user_topic_type = user_topic_type
        # self._agent_topic_type = agent_topic_type

    @message_handler
    async def handle_hello2_message(
        self, message: Hello2Message, ctx: MessageContext
    ) -> None:
        logger.info(f"{'-'*80}\nReceived hello2 message in session: {self.id.key}")
        logger.info(f"Message content: {message.content}")
        response = f"Hello2 agent received: {message.content}"
        logger.info(response)
        await self.publish_message(
            UserTask(context=message.context),
            topic_id=TopicId(message.reply_to_topic_type, source=self.id.key),
        )
        # return {"content": response}
