from collections.abc import Iterable
from typing import TYPE_CHECKING

from fastapi.encoders import jsonable_encoder
from langgraph.graph import StateGraph
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from sqlmodel import Session

from mtmai.models.models import User
from mtmai.mtlibs import aisdk

from .nodes import Nodes
from .state import EmailsState

if TYPE_CHECKING:
    from langchain_core.runnables.config import RunnableConfig


class WorkFlowCrewAgent:
    def __init__(self):
        nodes = Nodes()
        workflow = StateGraph(EmailsState)

        workflow.add_node("check_new_emails", nodes.check_email)
        # workflow.add_node("wait_next_run", nodes.wait_next_run)
        # workflow.add_node("draft_responses", EmailFilterCrew().kickoff)

        workflow.set_entry_point("check_new_emails")
        # workflow.add_conditional_edges(
        #     "check_new_emails",
        #     nodes.new_emails,
        #     {"continue": "draft_responses", "end": "wait_next_run"},
        # )
        # workflow.add_edge("draft_responses", "wait_next_run")
        # workflow.add_edge("wait_next_run", "check_new_emails")
        self.app = workflow.compile()

    @property
    def name(self):
        return "graphcrewdemo"

    async def chat(
        self,
        messages: Iterable[ChatCompletionMessageParam],
        db: Session,
        conversation_id: str | None = None,
        user: User | None = None,
    ):
        wf = self.app
        thread_id = "1"
        input = EmailsState(
            # messages=messages
            checked_emails_ids=["emailid123", "emailid234"]
        )
        config: RunnableConfig = {"configurable": {"thread_id": thread_id}}
        async for event in wf.astream_events(
            input=input,
            version="v2",
            config=config,
        ):
            kind = event["event"]
            name = event["name"]
            data = event["data"]
            if kind == "on_chat_model_stream":
                print("------")
                print(event["data"]["chunk"].dict())
                content = event["data"]["chunk"].content
                if content:
                    yield aisdk.text(content)
                # yield aisdk.text(content)
            print(f"astream_event: kind: {kind}, name={name},{data}")

            if kind == "on_chain_end" and name == "LangGraph":
                # 完全结束可以拿到最终数据
                # yield f"2: {json.dumps(jsonable_encoder(data))}\n"
                yield aisdk.data(jsonable_encoder(data))

        yield aisdk.finish()
