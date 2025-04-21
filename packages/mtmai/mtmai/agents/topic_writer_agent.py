from google.adk.agents import Agent
from mtmai.model_client.utils import get_default_litellm_model

TOPIC_WRITER_AGENT_PROMPT = """
你是seo专家,根据用户给定的主题,生成一个主题
重要:
    不到迫不得已, 应自己思考尽量完成任务,二不要想用户咨询各种选择
"""


def new_topic_writer_agent():
    return Agent(
        model=get_default_litellm_model(),
        name="topic_writer_agent",
        description="根据用户给定的主题,生成一个主题",
        instruction=TOPIC_WRITER_AGENT_PROMPT,
        tools=[
            # go_to_url,
            # take_screenshot,
            # find_element_with_text,
            # click_element_with_text,
            # enter_text_into_element,
            # scroll_down_screen,
            # get_page_source,
            # load_artifacts_tool,
            # analyze_webpage_and_determine_action,
        ],
    )
