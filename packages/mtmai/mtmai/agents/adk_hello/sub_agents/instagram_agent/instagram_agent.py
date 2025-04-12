from typing import Any, Optional

from google.adk.agents import Agent
from google.adk.tools import BaseTool
from google.adk.tools.tool_context import ToolContext
from mtmai.model_client.utils import get_default_litellm_model
from mtmai.tools.instagram_tool import (
    instagram_account_info,
    instagram_follow_user,
    instagram_login,
    instagram_write_post,
)

seed_users = [
    "yumeka64002",
    "a_ka.ri_3",
    # "ri.sa_0826",
    # "nobuko008",
    # "ayu55273",
    # "yuki_rax00x",
    # "m_i_yu_1102",
    # "anna1199aa",
    # "ric.odesu",
    # "elena_chan063",
    # "foxingbutsu",
    # "motoka556",
    # "4619.hina",
    # "sushengziyuan73",
    # sachi_ura_ako
    # momo.y0325
    # nakamura.tomoko1970
    # sayo_cha0
    # an_ni7571
    # mikuch35
    # kuru.mi9511
    # sayuri78263
    # chiyota_1524
    # yukino98221
    # sukurakawai13014
    # zi.yun14013
    # sayakadamii
    # miporin.0923
    # ayako.0229
    # manami_no_ura
    # yuu_nn000
    # minaaa50789
    # anna1199aa
    # miwa93218
    # kaor.iyanyan
    # rori0160
    # no_rik00
    # kawademikako
    # kanae_15758
    # haruru_ch
    # rina.18562
    # kyouko_music0829
    # laiaitianmeisha
    # usachan0712
    # yabunakahiroko4
    # miyuki20245
    # eunjoo1168
    # mikamikadesuyo
    # mik_ki0124
    # yurikoxt
    # kannachocho
    # nana_.xill
    # ayumienko
    # marn_na_94
    # mi_kki.3621
    # yuuna.x.ura
    # yuino.__1
    # kihoho77
    # reika_nt
    # 12460725a.sara
    # hiyori_2999
    # chie_7979
    # kumiko_823
    # 126656a.eina
    # yukie_desuyo
    # kaori_09.13
    # 19865413a.moe
    # rrr__iip
    # ai_uradazo
    # rin3.833
    # omg_boy.n
    # fumino.ig
    # kanako.440
    # kayosan67
    # ayaka_rin8
    # kana.ura01
    # naonoona
    # reirei_1118v
    # manamoo80
    # aikato.asobitai1
    # hina29500
    # kan_chandayo
    # shiratorimomoko1111
]

INSTAGRAM_AGENT_PROMPT = """你是 instagram 社交媒体操作的专家
背景:
    你拥有登录到 instagram 的账户基本信息,通过工具调用可以完成 instagram 的登录,以及登录后对账号的操作
    你是一个经验丰富的instagram 社交媒体操作专家, 你将使用 instagram 的 api 来操作 instagram 的账户
    根据用户的指令完成跟 instagram 相关的操作

## 工具调用
    - login_to_instagram: 登录到 instagram 的账户
    - post_to_instagram: 在 instagram 上发布帖子
    - instagram_follow_user: 关注其他用户
    - instagram_account_info: 获取当前用户信息

步骤建议:
    1: 登录到 instagram 的账户. 登录成功后, 保存登录信息到 state 中.
    2: 根据用户的指令完成跟 instagram 相关的操作.
    3: 当任务完成,或者出错无法继续时, 交接到 root_agent, 并且说明原因.
"""


def after_tool_callback(
    tool: BaseTool,
    args: dict[str, Any],
    tool_context: ToolContext,
    tool_response: dict[str, Any] = None,
) -> Optional[dict]:
    if tool.name == "instagram_login":
        if tool_response["success"]:
            tool_context.state.update({"ig_settings": tool_response["result"]})

            # --- Define State Changes ---
            # current_time = time.time()
            # state_changes = {
            #     "task_status": "active",  # Update session state
            #     "user:login_count": tool_context.state.get("user:login_count", 0)
            #     + 1,  # Update user state
            #     "user:last_login_ts": current_time,  # Add user state
            #     "temp:validation_needed": True,  # Add temporary state (will be discarded)
            # }

            # # --- Create Event with Actions ---
            # actions_with_update = EventActions(state_delta=state_changes)
            # # This event might represent an internal system action, not just an agent response
            # system_event = Event(
            #     invocation_id="inv_login_update",
            #     author="system",  # Or 'agent', 'tool' etc.
            #     actions=actions_with_update,
            #     timestamp=current_time,
            #     # content might be None or represent the action taken
            # )
            # return system_event

            # --- Append the Event (This updates the state) ---
            # session_service.append_event(session, system_event)
    if tool.name == "instagram_account_info":
        if tool_response["success"]:
            # tool_context.state["user_info"] = tool_response["result"]
            tool_context.state.update({"user_info": tool_response["result"]})
    return None


def new_instagram_agent():
    return Agent(
        model=get_default_litellm_model(),
        name="instagram_agent",
        description="跟 instagram 社交媒体操作的专家",
        instruction=INSTAGRAM_AGENT_PROMPT,
        tools=[
            instagram_login,
            instagram_write_post,
            instagram_account_info,
            instagram_follow_user,
        ],
        after_tool_callback=after_tool_callback,
    )
