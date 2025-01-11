import logging

from langchain_core.messages import ChatMessage
from langchain_core.runnables import Runnable, RunnableConfig

from mtmai.agents.states.state import MainState

logger = logging.getLogger()


def edge_mtmeditor(state: MainState):
    return "uidelta"


class MtmEditorNode:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    async def __call__(self, state: MainState, config: RunnableConfig):
        thread_id = config.get("configurable").get("thread_id")

        user_input = state.get("user_input")
        user_option = state.get("user_option")
        if user_option:
            # 是可视化编辑器的指令
            return {"go_mtmeditor": True}
        if user_input == "":
            logger.info("前端页面刷新后重新获取状态")
        if user_input.startswith("/"):
            return await self.uicommand(state, config)

        messages = state.get("messages")
        if len(messages) < 1:
            raise Exception("消息长度不正确")  # noqa: EM101, TRY002
        llm = self.runnable
        if messages[-1].type == "tool":
            ai_message = await llm.ainvoke(messages, config)
            return {
                "messages": [
                    ai_message,
                ],
            }
        new_user_message = ChatMessage(role="user", content=state.get("user_input"))
        messages.append(new_user_message)
        ai_message = await llm.ainvoke(messages, config)
        finnal_state = {
            "messages": [
                new_user_message,
                ai_message,
            ],
            "uidelta": state.get("uidelta"),
        }
        return finnal_state

    async def uicommand(self, state: MainState, config: RunnableConfig):
        user_input = state.get("user_input")
        return {}
