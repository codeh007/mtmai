import time
from textwrap import dedent
from typing import AsyncGenerator, List, Union

from google.adk.agents import BaseAgent, LlmAgent, SequentialAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from google.adk.models import BaseLlm
from google.genai import types  # noqa: F401
from pydantic import BaseModel, Field
from typing_extensions import override

from mtmai.model_client.utils import get_default_litellm_model


class ChapterOutline(BaseModel):
    title: str
    description: str


class BookOutline(BaseModel):
    chapters: List[ChapterOutline]


class Chapter(BaseModel):
    title: str
    content: str


class BookState(BaseModel):
    id: str = Field(default="1")
    title: str = Field(default="The Current State of AI in September 2024")
    book: List[Chapter] = Field(default_factory=list)
    book_outline: List[ChapterOutline] = Field(default_factory=list)
    topic: str = Field(
        default="Exploring the latest trends in AI across different industries as of September 2024"
    )
    goal: str = Field(
        default="""
        The goal of this book is to provide a comprehensive overview of the current state of artificial intelligence in September 2024.
        It will delve into the latest trends impacting various industries, analyze significant advancements,
        and discuss potential future developments. The book aims to inform readers about cutting-edge AI technologies
        and prepare them for upcoming innovations in the field.
    """
    )


class BookWriterAgent(BaseAgent):
    """
    书本写作代理
    """

    model_config = {"arbitrary_types_allowed": True}
    max_steps: int = Field(default=20)
    verbosity_level: int = Field(default=2)
    additional_authorized_imports: list[str] = Field(default_factory=lambda: ["*"])
    model: Union[str, BaseLlm] | None = Field(default=None)

    def __init__(
        self,
        name: str,
        description: str = "书本写作代理",
        max_steps: int = 20,
        verbosity_level: int = 2,
        additional_authorized_imports: list[str] = ["*"],
        model: Union[str, BaseLlm] | None = None,
    ):
        super().__init__(
            name=name,
            description=description,
            max_steps=max_steps,
            verbosity_level=verbosity_level,
            additional_authorized_imports=additional_authorized_imports,
            model=model or get_default_litellm_model(),
        )

    async def _init_state(self, ctx: InvocationContext):
        state = ctx.session.state.get("book_state")
        if state is None:
            state = BookState().model_dump()
            # --- 创建带有 Actions 的事件 ---
            actions_with_update = EventActions(state_delta=state)
            # 此事件可能代表内部系统操作，而不仅仅是智能体响应
            system_event = Event(
                invocation_id="inv_book_writer_update",
                author="system",  # 或 'agent', 'tool' 等
                actions=actions_with_update,
                timestamp=time.time(),
                # content 可能为 None 或表示所采取的操作
            )
            ctx.session_service.append_event(ctx.session, system_event)
        return state

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        # --- 定义状态更改 ---
        # current_time = time.time()
        # state_changes = {
        #     "book_state": BookState().model_dump(),
        # }
        # # --- 创建带有 Actions 的事件 ---
        # actions_with_update = EventActions(state_delta=state_changes)
        # # 此事件可能代表内部系统操作，而不仅仅是智能体响应
        # system_event = Event(
        #     invocation_id="inv_book_writer_update",
        #     author="system",  # 或 'agent', 'tool' 等
        #     actions=actions_with_update,
        #     timestamp=current_time,
        #     # content 可能为 None 或表示所采取的操作
        # )
        # ctx.session_service.append_event(ctx.session, system_event)

        book_state = await self._init_state(ctx)

        outline_writer_agent = LlmAgent(
            name="BookOutlineWriterAgent",
            description="书本章节写作, 在主题和大纲已经确定的情况下, 使用工具, 生成章节",
            model=self.model,
            instruction=dedent("""
                Role: Book Outlining Agent

                backstory:
                You are a skilled organizer, great at turning scattered information into a structured format.
                Your goal is to create clear, concise chapter outlines with all key topics and subtopics covered.

                Goal:
                Based on the research, generate a book outline about the following topic: {book_state.topic}
                The generated outline should include all chapters in sequential order and provide a title and description for each chapter.
                Here is some additional information about the author's desired goal for the book:\n\n {book_state.goal}
                """),
        )

        chapter_writer_agent = LlmAgent(
            name="BookChapterWriterAgent",
            description="书本章节写作, 在主题和大纲已经确定的情况下, 使用工具, 生成章节",
            model=self.model,
            instruction=dedent("""
                Role: Book Chapter Writer Agent

                Goal:
                Based on the book outline, generate a chapter about the following topic: {book_state.topic}
                """),
        )

        # --- 2. Create the SequentialAgent ---
        # 第一步: 根据话题, 进行调用,后编写书本大纲
        # 第二步: 根据大纲, 根据大纲, 使用工具, 生成章节
        book_pipeline_agent = SequentialAgent(
            name="BookPipelineAgent",
            sub_agents=[outline_writer_agent, chapter_writer_agent],
        )

        async for event in book_pipeline_agent.run_async(ctx):
            yield event
