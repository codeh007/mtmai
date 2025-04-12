import pyotp
from fastapi.encoders import jsonable_encoder
from google.adk.tools import ToolContext

from mtmai.core.config import settings
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
    # def forward(self, task: str):
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

    if tool_context.state.get("ig_settings"):
        # 如果已经登录过, 直接返回登录信息
        return {
            "success": True,
            "result": tool_context.state["ig_settings"],
        }
    if not username or not password:
        return {
            "success": False,
            "result": "username or password is empty",
        }

    ig_client = _get_ig_client(tool_context)
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
            return {
                "success": True,
                "result": login_data,
            }
    except Exception as e:
        # logger.error(f"instagram_login_tool: {e}")
        # return f"instagram login failed, reason: {e}"
        return {
            "success": False,
            "result": f"instagram login failed, reason: {e}",
        }


def instagram_follow_user(user_id: str, tool_context: ToolContext):
    """
    关注 instagram 用户.
    """
    ig_client = _get_ig_client(tool_context)

    try:
        ok = ig_client.user_follow(user_id)
        if ok:
            return {
                "success": True,
                "result": "instagram follow user success",
            }
        else:
            return {
                "success": False,
                "result": "instagram follow user failed",
            }
    except Exception as e:
        return {
            "success": False,
            "result": f"instagram follow user failed, reason: {e}",
        }


def instagram_write_post(post_content: str, tool_context: ToolContext):
    """
    在 instagram 上发布帖子.
    """
    ig_client = _get_ig_client(tool_context)

    ig_client.post_to_instagram(post_content)
    return "instagram post success"


def instagram_account_info(tool_context: ToolContext):
    """
    获取 instagram 当前用户信息.
    Args:
        user_id (str): The instagram user id.
        tool_context: ToolContext object.
    Returns:
        string: The instagram login result.
    """
    # user_id = (
    #     tool_context.state.get("ig_settings", {})
    #     .get("authorization_data", {})
    #     .get("ds_user_id")
    # )
    # if not user_id:
    #     return {
    #         "success": False,
    #         "result": "user_id is not set",
    #     }

    ig_settings = tool_context.state.get("ig_settings", None)
    if not ig_settings:
        return {
            "success": False,
            "result": "ig_settings is not set",
        }

    ig_client = _get_ig_client(tool_context)
    try:
        user_info = ig_client.account_info()
        return {
            "success": True,
            "result": jsonable_encoder(user_info.model_dump()),
        }
    except Exception as e:
        # debug_traceback(e)
        # return {
        #     "success": False,
        #     "result": f"instagram user info failed, reason: {e}",
        # }
        raise e


def _get_ig_client(tool_context: ToolContext):
    ig_client = Client(
        proxy=settings.default_proxy_url,
    )
    if tool_context.state.get("ig_settings"):
        ig_client.set_settings(tool_context.state["ig_settings"])
    return ig_client
