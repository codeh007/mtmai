from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig

from mtmai.agents.ctx import mtmai_context
from mtmai.agents.opencanvas.opencanvas_state import OpenCanvasState

WORK_DIR_NAME = "project"
WORK_DIR = f"/home/{WORK_DIR_NAME}"
MODIFICATIONS_TAG_NAME = "bolt_file_modifications"


class RespondToQueryNode:
    async def __call__(self, state: OpenCanvasState, config: RunnableConfig):
        user_id = state.userId
        params = state.params
        messages = state.messages
        assistant_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an AI assistant tasked with responding to the users question.

The user has generated artifacts in the past. Use the following artifacts as context when responding to the users question.

You also have the following reflections on style guidelines and general memories/facts about the user to use when generating your response.
<reflections>
{reflections}
</reflections>

<artifacts>
{artifacts}
</artifacts>""",
                ),
                ("placeholder", "{messages}"),
            ]
        ).partial(
            reflections="",
            artifacts="",
            messages=messages,
        )
        aiMsg = await mtmai_context.ainvoke_model(assistant_prompt, state, tools=[])
        return {"messages": aiMsg}
