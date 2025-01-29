from dataclasses import dataclass
from typing import Any, Dict, Optional

from autogen_agentchat.agents import AssistantAgent
from autogen_core import (
    AgentId,
    DefaultTopicId,
    MessageContext,
    RoutedAgent,
    SingleThreadedAgentRuntime,
    default_subscription,
    message_handler,
)
from autogen_core.model_context import BufferedChatCompletionContext
from autogen_core.models import (
    AssistantMessage,
    ChatCompletionClient,
    SystemMessage,
    UserMessage,
)

from .model_client import get_oai_Model
from .termination_handler import termination_handler


class LoggingAssistantAgent(AssistantAgent):
    """扩展AssistantAgent以添加日志功能"""

    async def _process_received_message(self, message: Dict[str, Any]) -> Optional[str]:
        return await super()._process_received_message(message)

    async def run(self, *args, **kwargs):
        try:
            result = await super().run(*args, **kwargs)
            return result
        except Exception:
            raise


@dataclass
class Message:
    content: str


@default_subscription
class Assistant(RoutedAgent):
    def __init__(self, name: str, model_client: ChatCompletionClient) -> None:
        super().__init__("An assistant agent.")
        self._model_client = model_client
        self.name = name
        self.count = 0
        self._system_messages = [
            SystemMessage(
                content=f"Your name is {name} and you are a part of a duo of comedians."
                "You laugh when you find the joke funny, else reply 'I need to go now'.",
            )
        ]
        self._model_context = BufferedChatCompletionContext(buffer_size=5)

    @message_handler
    async def handle_message(self, message: Message, ctx: MessageContext) -> None:
        self.count += 1
        await self._model_context.add_message(
            UserMessage(content=message.content, source="user")
        )
        result = await self._model_client.create(
            self._system_messages + await self._model_context.get_messages()
        )

        print(f"\n{self.name}: {message.content}")

        if "I need to go".lower() in message.content.lower() or self.count > 2:
            return

        await self._model_context.add_message(
            AssistantMessage(content=result.content, source="assistant")
        )  # type: ignore
        await self.publish_message(Message(content=result.content), DefaultTopicId())  # type: ignore


async def hello_ag_run() -> None:
    agent = LoggingAssistantAgent(
        "blog_writer",
        model_client=get_oai_Model(),
        system_message="""你是一位极具洞察力的科技博主，擅长:
        1. 发现和分享AI领域最新、最有趣的应用和趋势
        2. 用生动的案例和数据支撑观点
        3. 提供独特的见解和实用的建议
        4. 善于用故事化的写作方式吸引读者
        请确保内容既专业又有趣，让读者感受到实用价值。""",
    )

    blog_prompt = """请写一篇引人入胜的博客文章，要求：
    1. 主题：选择以下任一个具体角度切入AI在日常生活中的应用：
       - "我用AI重新设计了我的早晨routine，发生了这些改变..."
       - "为什么说2024年是普通人入门AI的最佳时机"
       - "我用AI帮我做副业赚钱的一个月：经验和教训"
    2. 写作要求：
       - 开头要有吸引人的hook，比如一个有趣的故事或令人意外的数据
       - 分享真实可行的经验和洞察，而不是泛泛而谈
       - 每个观点都要配合具体的例子或数据
       - 提供实用的行动建议，读者看完就能上手尝试
       - 结尾要有清晰的call-to-action
    3. 结构：
       - 引言：吸引人的开场 + 文章价值预告
       - 正文：3-4个核心观点，每个配有实例
       - 总结：核心观点提炼 + 行动建议
    4. 字数：1500字左右，确保内容充实
    5. 风格：轻松但专业，像朋友分享经验一样自然
    """

    try:
        # 直接调用 agent
        result = await agent.run(task=blog_prompt)
        print(result)
        # llm_usage 有额外的跟踪信息
    except Exception:
        # logger.error("生成文章时发生错误", exc_info=True)
        raise

    # 通过 runtime 调用agent
    runtime = SingleThreadedAgentRuntime(intervention_handlers=[termination_handler])
    cathy = await Assistant.register(
        runtime,
        "cathy",
        lambda: Assistant(name="Cathy", model_client=get_oai_Model()),
    )

    joe = await Assistant.register(
        runtime,
        "joe",
        lambda: Assistant(name="Joe", model_client=get_oai_Model()),
    )

    runtime.start()
    await runtime.send_message(
        Message("Joe, tell me a joke."),
        recipient=AgentId(joe, "default"),
        sender=AgentId(cathy, "default"),
    )
    await runtime.stop_when_idle()
