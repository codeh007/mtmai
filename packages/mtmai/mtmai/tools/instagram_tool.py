import pyotp
from google.adk.tools import ToolContext
from mtmai.core.config import settings
from mtmai.mtlibs.adk_utils.adk_utils import tool_success
from mtmai.mtlibs.instagrapi import Client


def _get_ig_client(tool_context: ToolContext):
    ig_client = Client(
        proxy=settings.default_proxy_url,
    )
    if tool_context.state.get("ig_settings"):
        ig_client.set_settings(tool_context.state["ig_settings"])
    return ig_client


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
        if ok:
            login_data = ig_client.get_settings()
            return {
                "success": True,
                "result": login_data,
            }
    except Exception as e:
        return {
            "success": False,
            "result": f"instagram login failed, reason: {e}",
        }


def instagram_follow_user(username: str, tool_context: ToolContext):
    """
    关注 instagram 用户.
    Args:
        username (str): The instagram user name.
        tool_context: ToolContext object.
    Returns:
        string: The instagram login result.
    """
    ig_client = _get_ig_client(tool_context)

    user_id = ig_client.user_id_from_username(username)

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
    ig_settings = tool_context.state.get("ig_settings", None)
    if not ig_settings:
        return {
            "success": False,
            "result": "ig_settings is not set",
        }

    try:
        ig_client = _get_ig_client(tool_context)
        user_info = ig_client.account_info()
        return tool_success(user_info)
    except Exception as e:
        # debug_traceback(e)
        # return {
        #     "success": False,
        #     "result": f"instagram user info failed, reason: {e}",
        # }
        raise e
