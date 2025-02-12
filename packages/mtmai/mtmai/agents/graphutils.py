from typing import Callable

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.runnables import Runnable, RunnableLambda
from langgraph.prebuilt import ToolNode
from pydantic import BaseModel
def handle_tool_error(state) -> dict:
    error = state.get("error")
    tool_calls = state.messages[-1].tool_calls
    return {
        "messages": [
            ToolMessage(
                content=f"Error: {error!r}\n please fix your mistakes.",
                tool_call_id=tc["id"],
            )
            for tc in tool_calls
        ]
    }


def create_tool_node_with_fallback(tools: list):
    return ToolNode(tools).with_fallbacks(
        [RunnableLambda(handle_tool_error)],
        # exception_key="error"
    )


def _print_event(event: dict, _printed: set, max_length=1500):
    current_state = event.get("dialog_state")
    if current_state:
        print("Currently in: ", current_state[-1])
    message = event.get("messages")
    if message:
        if isinstance(message, list):
            message = message[-1]
        if message.id not in _printed:
            msg_repr = message.pretty_repr(html=True)
            if len(msg_repr) > max_length:
                msg_repr = msg_repr[:max_length] + " ... (truncated)"
            print(msg_repr)
            _printed.add(message.id)


def agent_node(state, agent, name):
    result = agent.invoke(state)
    return {
        "messages": [HumanMessage(content=result["messages"][-1].content, name=name)]
    }


class CompleteOrEscalate(BaseModel):
    """A tool to mark the current task as completed and/or to escalate control of the dialog to the main assistant,
    who can re-route the dialog based on the user's needs."""

    cancel: bool = True
    reason: str

    class Config:
        json_schema_extra = {
            "example": {
                "cancel": True,
                "reason": "User changed their mind about the current task.",
            },
            "example 2": {
                "cancel": True,
                "reason": "I have fully completed the task.",
            },
            "example 3": {
                "cancel": False,
                "reason": "I need to search the user's emails or calendar for more information.",
            },
        }


async def ensure_valid_llm_response_v2(runnable: Runnable, messages: list):
    """
    确保 LLM 返回有效的回应
    原理：如果 LLM 返回了空内容，就主动模拟用户输入新的消息："Respond with a real output."
         催促 LLM 重新给出回应
    """

    messages_inner = list(messages)
    while True:
        ai_msg = await runnable.ainvoke(messages_inner)

        if isinstance(ai_msg, AIMessage):
            ai_msg_to_check = ai_msg.model_dump()
        else:
            ai_msg_to_check = ai_msg
        if (
            # ("parsed" not in ai_msg or not ai_msg["parsed"])
            ai_msg_to_check.get("parsed", None) is None
            and ai_msg_to_check.get("tool_calls", None) is not None
            and (
                ai_msg_to_check.get("content", None) is None
                or isinstance(ai_msg_to_check.get("content", None), list)
                and ai_msg_to_check.get("content", None)[0].get("text") is None
            )
        ):
            messages_inner = messages_inner + [("user", "Respond with a real output.")]
        else:
            break
    return ai_msg

internal_node_types = set(
    [
        "RunnableSequence",
        "RunnableLambda",
        "RunnableParallel<raw>",
        "RunnableWithFallbacks",
        "_write",
        "start",
        "end",
    ]
)
skip_kinds = set(
    [
        "on_tool_start",
        "on_tool_end",
        "on_chat_model_stream",
    ]
)

def is_internal_node(node_name: str):
    """
    判断是否是内部节点
    """
    return node_name in internal_node_types


def is_skip_kind(kind: str):
    """
    判断是否是跳过类型
    """
    return kind in skip_kinds
