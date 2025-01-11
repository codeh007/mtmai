from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.runnables import Runnable, RunnableConfig

from mtmai.core.logging import get_logger
from mtmai.models.graph_config import HomeChatState, InterviewState

logger = get_logger()


def swap_roles(state: InterviewState, name: str):
    converted = []
    for message in state["messages"]:
        if isinstance(message, AIMessage) and message.name != name:
            message = HumanMessage(**message.dict(exclude={"type"}))
        converted.append(message)
    return {"messages": converted}


class Assistant:
    def __init__(self, runnable: Runnable):
        self.runnable = runnable

    def __call__(self, state: HomeChatState, config: RunnableConfig):
        while True:
            result = self.runnable.invoke(state)

            if not result.tool_calls and (
                not result.content
                or isinstance(result.content, list)
                and not result.content[0].get("text")
            ):
                messages = state.messages + [("user", "Respond with a real output.")]
                state = {**state, "messages": messages}
            else:
                break
        return {"messages": result}


# class CompleteOrEscalate(BaseModel):
#     """A tool to mark the current task as completed and/or to escalate control of the dialog to the main assistant,
#     who can re-route the dialog based on the user's needs."""

#     cancel: bool = True
#     reason: str

#     class Config:
#         json_schema_extra = {
#             "example": {
#                 "cancel": True,
#                 "reason": "User changed their mind about the current task.",
#             },
#             "example 2": {
#                 "cancel": True,
#                 "reason": "I have fully completed the task.",
#             },
#             "example 3": {
#                 "cancel": False,
#                 "reason": "I need to search the user's emails or calendar for more information.",
#             },
#         }
