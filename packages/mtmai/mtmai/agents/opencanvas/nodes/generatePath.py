from datetime import datetime

from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from pydantic import BaseModel

from mtmai.agents.ctx import mtmai_context
from mtmai.agents.opencanvas.opencanvas_state import OpenCanvasState
from mtmai.core.logging import get_logger

logger = get_logger()


class RouteQueryResult(BaseModel):
    route: str
    artifactId: str | None = None


def routeGeneratePath(state: OpenCanvasState):
    # is_tools = tools_condition(state)
    # if is_tools == "tools":
    #     return "chat_tools_node"
    if not state.next:
        raise ValueError("state.next not set")
    # next_to = state.get("next")
    # if next_to:
    #     return next_to
    return state.next


class GeneratePath:
    """
    根据状态选择下一节点
    """

    def __init__(self):
        pass

    async def __call__(self, state: OpenCanvasState, config: RunnableConfig):
        # 临时代码
        # 展示一直置项 SiteNode
        # return {
        #     "next": "SiteNode",
        # }
        messages = state.messages

        # 如果有明确的状态，例如用户选定了一些文字，选定了一些组件。
        if state.highlighted:
            return {
                "next": "updateArtifact",
                "selectedArtifactId": state.highlighted.id,
            }

        # 如果没有明确状态，就调用 llm 决定下一个节点
        parser = PydanticOutputParser(pydantic_object=RouteQueryResult)

        route_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """You are an assistant tasked with routing the users query based on their most recent message.
You should look at this message in isolation and determine where to best route there query.
Your options are as follows:

- 'updateArtifact': The user has requested some sort of change or edit to an existing artifact. Use their recent message and the currently selected artifact (if any) to determine what to do. You should ONLY select this if the user has clearly requested a change to the artifact, otherwise you should lean towards either generating a new artifact or responding to their query.
  It is very important you do not edit the artifact unless clearly requested by the user.
- 'generateArtifact': The user has inputted a request which requires generating a new artifact.
  Artifacts can be any sort of writing content, code, or other creative works. Think of artifacts as content you might find on a blog, google doc, or other writing platform.
- 'respondToQuery': The user has asked a question, or has submitted a general message which requires a response, but does not require updating or generating an entirely new artifact.

If you believe the user wants to update an existing artifact, you MUST also supply the ID of the artifact they are referring to.

A few of the recent messages in the chat history are:
<recent-messages>
{recentMessages}
</recent-messages>

The following contains every artifact the user has generated in the chat history:
<artifacts>determinant
{artifacts}compare
</artifacts>move
tee
This artifact is the one the user is currently viewing. You should weigh this artifact more heavily compared to the others when determining the route.
<selected-artifact>
{selectedArtifact}
</selected-artifact>""",
                ),
                # ("placeholder", "{messages}"),
            ]
        ).partial(
            time=datetime.now(),
            recentMessages=messages,
            artifacts="",
            selectedArtifact="",
        )

        result = await mtmai_context.ainvoke_model_with_structured_output(
            route_prompt,
            state,
            structured_output=RouteQueryResult,
        )
        if result is None:
            return {
                "next": "respondToQuery",
            }
        next = result["parsed"].route
        if next == "updateArtifact":
            selectedArtifactId = result.artifactId
        return {
            "next": next,
        }
