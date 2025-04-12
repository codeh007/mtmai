import pyotp
from google.adk.tools import ToolContext
from loguru import logger

from mtmai.mtlibs.instagrapi import Client


def instagram_login(
    username: str, password: str, otp_key: str, tool_context: ToolContext
):
    """
    根据用户名密码登录 instagram, 其中 otp_key 是可选的, 如果需要使用两步验证的话.

    Args:
        username (str): The instagram username.
        password (str): The instagram password.
        otp_key (str): The instagram otp key.
        tool_context: ToolContext object.
    Returns:
        string: The instagram login result.
    """
    logger.info(f"instagram_login_tool: {username}, {password}, {otp_key}")
    # name = "instagram_login"
    # description = """登录 instagram
    # """
    # inputs = {
    #     "task": {
    #         "type": "string",
    #         "description": "the task category (such as text-classification, depth-estimation, etc)",
    #     }
    # }
    # output_type = "string"

    # def forward(self, task: str):
    #     IG_USERNAME = ""
    #     IG_PASSWORD = ""
    #     IG_CREDENTIAL_PATH = "./ig_settings.json"
    #     # SLEEP_TIME = "600"  # in seconds

    #     ig_client = Client()
    #     ig_client.login(IG_USERNAME, IG_PASSWORD)
    #     ig_client.dump_settings(IG_CREDENTIAL_PATH)

    #     userid = ig_client.user_id_from_username("hello")
    #     ig_client.user_follow(userid)
    #     ig_client.user_unfollow(userid)
    #     ig_client.user_followers(userid, amount=10)
    #     ig_client.user_following(userid, amount=10)
    #     ig_client.user_followers_full(userid, amount=10)

    username = username.strip()
    password = password.strip()
    otp_key = otp_key.strip().replace(" ", "")
    ig_client = Client()
    try:
        ok = ig_client.login(
            username,
            password,
            verification_code=pyotp.TOTP(otp_key).now(),
            relogin=False,
        )
        # current_time = time.time()
        # state_changes = {
        #     "task_status": "active",  # Update session state
        #     "user:login_count": tool_context.state.get("user:login_count", 0)
        #     + 1,  # Update user state
        #     "user:last_login_ts": current_time,  # Add user state
        #     "temp:validation_needed": True,  # Add temporary state (will be discarded)
        # }
        # actions_with_update = EventActions(state_delta=state_changes)
        # system_event = Event(
        #     invocation_id="inv_login_update",
        #     author="system",  # Or 'agent', 'tool' etc.
        #     actions=actions_with_update,
        #     timestamp=current_time,
        #     # content might be None or represent the action taken
        # )

        if ok:
            # return "instagram login success"
            login_data = ig_client.get_settings()
            return login_data
    except Exception as e:
        logger.error(f"instagram_login_tool: {e}")
        return f"instagram login failed, reason: {e}"


def instagram_write_post_tool(post_content: str):
    """
    在 instagram 上发布帖子.
    """
    ig_client = Client()
    ig_client.post_to_instagram(post_content)
    return "instagram post success"


def instagram_user_info_tool(user_id: str, tool_context: ToolContext):
    """
    获取 instagram 当前用户信息.
    Args:
        user_id (str): The instagram user id.
        tool_context: ToolContext object.
    Returns:
        string: The instagram login result.
    """
    ig_client = Client()
    user_info = ig_client.user_info(user_id)
    return user_info
