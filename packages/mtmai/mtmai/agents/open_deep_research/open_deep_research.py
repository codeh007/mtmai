# import os

from google.adk.tools import ToolContext

# from huggingface_hub import login
from mtmai.core.config import settings
from mtmai.model_client.utils import get_default_smolagents_model
from smolagents import CodeAgent, GoogleSearchTool, ToolCallingAgent

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

# login(os.getenv(settings.HF_TOKEN))


async def adk_open_deep_research_tool(
    question: str, tool_context: ToolContext
) -> dict[str, str]:
    """执行自主多步骤任务, 并返回最终结果,
        例如: question: 小牛电动车怎么样?
    Args:
        question: 问题描述
    Returns:
        最终答案
    """
    model = get_default_smolagents_model()
    text_limit = 100000

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
        model=model,
        tools=[
            GoogleSearchTool(provider="serper"),
            VisitTool(browser),
            PageUpTool(browser),
            PageDownTool(browser),
            FinderTool(browser),
            FindNextTool(browser),
            ArchiveSearchTool(browser),
            TextInspectorTool(model, text_limit),
        ],
        max_steps=20,
        verbosity_level=2,
        planning_interval=4,
        name="search_agent",
        description="""A team member that will search the internet to answer your question.
    Ask him for all your questions that require browsing the web.
    Provide him as much context as possible, in particular if you need to search on a specific timeframe!
    And don't hesitate to provide him with a complex search task, like finding a difference between two webpages.
    Your request must be a real sentence, not a google search! Like "Find me this information (...)" rather than a few keywords.
    """,
        provide_run_summary=True,
    )
    text_webbrowser_agent.prompt_templates["managed_agent"][
        "task"
    ] += """You can navigate to .txt online files.
    If a non-html page is in another format, especially .pdf or a Youtube video, use tool 'inspect_file_as_text' to inspect it.
    Additionally, if after some searching you find out that you need more information to answer the question, you can use `final_answer` with your request for clarification as argument to request for more information."""

    manager_agent = CodeAgent(
        model=model,
        tools=[visualizer, TextInspectorTool(model, text_limit)],
        max_steps=12,
        verbosity_level=2,
        additional_authorized_imports=["*"],
        planning_interval=4,
        managed_agents=[text_webbrowser_agent],
    )

    answer = manager_agent.run(question)
    return {"answer": answer}
