from google.adk.agents import Agent
from mtmai.model_client import get_default_litellm_model

CONTENT_WRITER_AGENT_PROMPT = """
你是擅长内容创作的专家,根据用户给定的主题,生成文章的正文
"""


def new_content_writer_agent():
    return Agent(
        model=get_default_litellm_model(),
        name="content_writer_agent",
        description="根据跟定的主题,生成文章的正文",
        instruction=CONTENT_WRITER_AGENT_PROMPT,
        tools=[],
    )
