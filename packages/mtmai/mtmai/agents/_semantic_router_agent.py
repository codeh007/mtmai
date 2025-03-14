from autogen_core import (
    DefaultTopicId,
    MessageContext,
    RoutedAgent,
    TopicId,
    message_handler,
)
from loguru import logger
from mtmai.agents._agents import (
    browser_topic_type,
    coder_agent_topic_type,
    team_runner_topic_type,
)
from mtmai.agents._types import (
    AgentRegistryBase,
    BrowserOpenTask,
    BrowserTask,
    CodeWritingTask,
    IntentClassifierBase,
    TeamRunnerTask,
    TerminationMessage,
)

# from mtmai.mtmpb.ag_pb2 import AgentRunInput
from mtmai.clients.rest.models.agent_run_input import AgentRunInput


class SemanticRouterAgent(RoutedAgent):
    def __init__(
        self,
        name: str,
        agent_registry: AgentRegistryBase,
        intent_classifier: IntentClassifierBase,
    ) -> None:
        super().__init__("Semantic Router Agent")
        self._name = name
        self._registry = agent_registry
        self._classifier = intent_classifier

    # The User has sent a message that needs to be routed
    @message_handler
    async def handle_route_to_agent(
        self, message: AgentRunInput, ctx: MessageContext
    ) -> None:
        assert ctx.topic_id is not None
        logger.info(f"Received message from {message.source}: {message.content}")
        session_id = ctx.topic_id.source

        user_content = message.content
        if user_content.startswith("/test_code"):
            await self._runtime.publish_message(
                message=CodeWritingTask(
                    task="Write a function to find the sum of all even numbers in a list."
                ),
                topic_id=TopicId(coder_agent_topic_type, source=session_id),
            )
        elif user_content.startswith("/test_open_browser"):
            await self._runtime.publish_message(
                message=BrowserOpenTask(url="https://playwright.dev/"),
                topic_id=TopicId(browser_topic_type, source=session_id),
            )
        elif user_content.startswith("/test_browser_task"):
            await self._runtime.publish_message(
                message=BrowserTask(task="Open an online code editor programiz."),
                topic_id=TopicId(browser_topic_type, source=session_id),
            )
        elif user_content.startswith("/test_team"):
            await self._runtime.publish_message(
                message=TeamRunnerTask(task=user_content, team=team_runner_topic_type),
                topic_id=TopicId(team_runner_topic_type, source=session_id),
            )
        else:
            # 意图识别
            # 意图识别, 通常用于同一个 type 的用户输入,根据路由规则, 找到最合适的agent
            # 关键点在于当有多个 agent 都能处理相同的 输入类型的时候,可以根据意图将用户的输入转发的**单个** agent
            intent = await self._identify_intent(message)
            # 找到最合适的agent
            agent = await self._find_agent(intent)
            # 联系agent
            await self.contact_agent(agent, message, session_id)

    ## Identify the intent of the user message
    async def _identify_intent(self, message: AgentRunInput) -> str:
        return await self._classifier.classify_intent(message.content)

    ## Use a lookup, search, or LLM to identify the most relevant agent for the intent
    async def _find_agent(self, intent: str) -> str:
        logger.debug(f"Identified intent: {intent}")
        try:
            agent = await self._registry.get_agent(intent)
            return agent
        except KeyError:
            logger.info("No relevant agent found for intent: " + intent)
            return "termination"

    ## Forward user message to the appropriate agent, or end the thread.
    async def contact_agent(
        self, agent: str, message: AgentRunInput, session_id: str
    ) -> None:
        if agent == "termination":
            logger.info("No relevant agent found")
            await self.publish_message(
                TerminationMessage(
                    reason="No relevant agent found",
                    content=message.content,
                    source=self.type,
                ),
                DefaultTopicId(type="user_proxy", source=session_id),
            )
        else:
            logger.debug("Routing to agent: " + agent)
            await self.publish_message(
                AgentRunInput(content=message.content, source=message.source),
                # DefaultTopicId(type=agent, source=session_id),
                TopicId(agent, source=session_id),
            )
