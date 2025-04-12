from google.adk.agents import Agent
from mtmai.model_client.utils import get_default_litellm_model

INSTAGRAM_AGENT_PROMPT = """你是跟 instagram 社交媒体操作的专家
背景:
    你拥有登录到 instagram 的账户基本信息,通过工具调用可以完成 instagram 的登录,以及登录后对账号的操作
    你是一个经验丰富的instagram 社交媒体操作专家, 你将使用 instagram 的 api 来操作 instagram 的账户
    根据用户的指令完成跟 instagram 相关的操作

## 工具调用
    - login_to_instagram: 登录到 instagram 的账户
    - post_to_instagram: 在 instagram 上发布帖子
    - follow_user: 关注其他用户
    - unfollow_user: 取消关注其他用户

步骤建议:
    1: 登录到 instagram 的账户.
    2: 根据用户的指令完成跟 instagram 相关的操作.
    3: 当任务完成,或者出错无法继续时, 交接到 root_agent, 并且说明原因.
"""


def login_to_instagram(username: str, password: str, otp_key: str):
    pass


def post_to_instagram(post_content: str):
    pass


def new_instagram_agent():
    return Agent(
        model=get_default_litellm_model(),
        name="instagram_agent",
        description="跟 instagram 社交媒体操作的专家",
        instruction=INSTAGRAM_AGENT_PROMPT,
        tools=[
            login_to_instagram,
            post_to_instagram,
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
