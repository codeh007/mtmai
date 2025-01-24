import asyncio
import logging
from typing import Any, Dict, Optional

from autogen_agentchat.agents import AssistantAgent
from autogen_core import EVENT_LOGGER_NAME
from autogen_ext.models.openai import OpenAIChatCompletionClient

from .trace import LLMUsageTracker

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("agent_execution.log"), logging.StreamHandler()],
)

# logger = logging.getLogger(__name__)

# Set up the logging configuration to use the custom handler
logger = logging.getLogger(EVENT_LOGGER_NAME)
logger.setLevel(logging.INFO)
llm_usage = LLMUsageTracker()
logger.handlers = [llm_usage]


class LoggingAssistantAgent(AssistantAgent):
    """扩展AssistantAgent以添加日志功能"""

    async def _process_received_message(self, message: Dict[str, Any]) -> Optional[str]:
        logger.info(f"收到消息: {message}")
        return await super()._process_received_message(message)

    async def run(self, *args, **kwargs):
        logger.info(f"Agent开始执行任务，参数: {args}, {kwargs}")
        try:
            result = await super().run(*args, **kwargs)
            logger.info(f"任务执行完成，结果长度: {len(str(result))}")
            return result
        except Exception as e:
            logger.error(f"任务执行出错: {str(e)}", exc_info=True)
            raise


def getOaiModel():
    model_client = OpenAIChatCompletionClient(
        model="llama3.3-70b",
        api_key="ZGd2VL8B9KxqMB3HIsTaNXmp5iM9ew3c",
        base_url="https://llama3-3-70b.lepton.run/api/v1/",
        model_info={
            "vision": False,
            "function_calling": True,
            "json_output": True,
            "family": "unknown",
        },
        # stream=True,
        max_tokens=8000,
        temperature=0.8,
    )
    return model_client


async def main() -> None:
    logger.info("开始初始化agent")

    agent = LoggingAssistantAgent(
        "blog_writer",
        getOaiModel(),
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
        # 使用 stream=True 来接收流式响应
        async for chunk in await agent.run(task=blog_prompt):
            if chunk:
                print(chunk, end="", flush=True)
        logger.info("文章生成成功")
    except Exception:
        logger.error("生成文章时发生错误", exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(main())
if __name__ == "__main__":
    asyncio.run(main())
