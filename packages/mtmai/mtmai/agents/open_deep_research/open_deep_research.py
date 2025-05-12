from textwrap import dedent
from typing import AsyncGenerator, Union

from google.adk.agents import LlmAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from google.adk.models import BaseLlm
from google.genai import types  # noqa: F401
from loguru import logger  # noqa: F401
from mtmai.core.config import settings
from mtmai.model_client import get_default_smolagents_model
from pydantic import Field
from smolagents import CodeAgent, GoogleSearchTool, ToolCallingAgent
from smolagents.memory import ActionStep, FinalAnswerStep, PlanningStep
from typing_extensions import override

from .scripts.text_inspector_tool import TextInspectorTool
from .scripts.text_web_browser import (
    ArchiveSearchTool,
    FinderTool,
    FindNextTool,
    PageDownTool,
    PageUpTool,
    SimpleTextBrowser,
    VisitTool,
)
from .scripts.visual_qa import visualizer


class AdkOpenDeepResearch(LlmAgent):
    model_config = {"arbitrary_types_allowed": True}
    text_limit: int = Field(default=100000, description="文本限制")
    max_steps: int = Field(default=25, description="最大步骤")
    verbosity_level: int = Field(default=2, description="日志级别")
    additional_authorized_imports: list[str] = Field(
        default=["*"], description="授权导入"
    )
    model: Union[str, BaseLlm] | None = None
    description: str = (
        "执行自主多步骤任务, 并返回最终结果, 例如: question: 小牛电动车怎么样?"
    )

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        user_content = ctx.user_content
        user_input_text = user_content.parts[0].text

        BROWSER_CONFIG = {
            "viewport_size": 1024 * 5,
            "downloads_folder": "downloads_folder",
            "serpapi_key": settings.SERPAPI_API_KEY,
            "request_kwargs": {
                "headers": {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0"
                },
                "timeout": 300,
            },
        }
        browser = SimpleTextBrowser(**BROWSER_CONFIG)
        text_webbrowser_agent = ToolCallingAgent(
            model=get_default_smolagents_model(),
            tools=[
                GoogleSearchTool(provider="serper"),
                VisitTool(browser),
                PageUpTool(browser),
                PageDownTool(browser),
                FinderTool(browser),
                FindNextTool(browser),
                ArchiveSearchTool(browser),
                TextInspectorTool(self.model, self.text_limit),
            ],
            max_steps=self.max_steps,
            verbosity_level=self.verbosity_level,
            planning_interval=4,
            name="search_agent",
            description=dedent("""A team member that will search the internet to answer your question.
        Ask him for all your questions that require browsing the web.
        Provide him as much context as possible, in particular if you need to search on a specific timeframe!
        And don't hesitate to provide him with a complex search task, like finding a difference between two webpages.
        Your request must be a real sentence, not a google search! Like "Find me this information (...)" rather than a few keywords.
        """),
            provide_run_summary=True,
        )
        text_webbrowser_agent.prompt_templates["managed_agent"]["task"] += (
            dedent("""You can navigate to .txt online files.
        If a non-html page is in another format, especially .pdf or a Youtube video, use tool 'inspect_file_as_text' to inspect it.
        Additionally, if after some searching you find out that you need more information to answer the question, you can use `final_answer` with your request for clarification as argument to request for more information.""")
        )

        code_agent = CodeAgent(
            model=get_default_smolagents_model(),
            tools=[visualizer, TextInspectorTool(self.model, self.text_limit)],
            max_steps=self.max_steps,
            verbosity_level=self.verbosity_level,
            additional_authorized_imports=self.additional_authorized_imports,
            planning_interval=4,
            managed_agents=[text_webbrowser_agent],
        )

        for step in code_agent.run(task=user_input_text, stream=True, reset=True):
            if isinstance(step, ActionStep):
                # logger.info(f"ActionStep: {step}")
                pass
            if isinstance(step, PlanningStep):
                # logger.info(f"PlanningStep: {step}")
                pass
            if isinstance(step, FinalAnswerStep):
                yield Event(
                    author=self.name,
                    content=types.Content(
                        role=self.name,
                        parts=[
                            types.Part(text=step.final_answer),
                        ],
                    ),
                )
        # 交接给父级 agent
        yield Event(
            author=self.name,
            actions=EventActions(
                transfer_to_agent="shortvideo_generator",
                # escalate=True,
            ),
        )
