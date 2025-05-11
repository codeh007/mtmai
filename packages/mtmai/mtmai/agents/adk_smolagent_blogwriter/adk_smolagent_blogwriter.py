from google.adk.tools import ToolContext
from mtmai.model_client import get_default_smolagents_model


async def adk_smolagent_blogwriter_tool(
    topic: str, tool_context: ToolContext
) -> dict[str, str]:
    """根据给定的主题, 生成博客文章, 工具本身是 ai agent,可以根据任务描述执行自主多步骤任务, 并返回最终结果,
        例如: topic: Create a blog post about the top 5 products released at CES 2025 so far. Please include specific product names and sources

    Args:
        topic: 博客主题
    Returns:
        操作的最终结果
    """
    from mtmai.tools.jinaai import scrape_page_with_jina_ai, search_facts_with_jina_ai
    from smolagents import CodeAgent, DuckDuckGoSearchTool, ToolCallingAgent

    # Research Agent
    research_agent = ToolCallingAgent(
        name="super_researcher",
        description="Researches topics thoroughly using web searches and content scraping. Provide the research topic as input.",
        tools=[
            scrape_page_with_jina_ai,
            search_facts_with_jina_ai,
            DuckDuckGoSearchTool(),
        ],
        model=get_default_smolagents_model(),
        max_steps=10,
    )
    # Research Checker Agent
    research_checker_agent = ToolCallingAgent(
        name="research_checker",
        description="Checks the research for relevance to the original task request. If the research is not relevant, it will ask for more research.",
        tools=[],
        model=get_default_smolagents_model(),
    )

    # Writer Agent
    writer_agent = ToolCallingAgent(
        name="writer",
        description="Writes blog posts based on the checkedresearch. Provide the research findings and desired tone/style.",
        tools=[],
        model=get_default_smolagents_model(),
    )

    # Copy Editor Agent
    copy_editor_agent = ToolCallingAgent(
        name="editor",
        description="Reviews and polishes the blog post based on the research and original task request. Order the final blog post and any lists in a way that is most engaging to someone working in AI. Provides the final, edited version in markdown.",
        tools=[],
        model=get_default_smolagents_model(),
    )

    # Main Blog Writer Manager
    blog_manager = CodeAgent(
        tools=[],
        model=get_default_smolagents_model(),
        managed_agents=[
            research_agent,
            research_checker_agent,
            writer_agent,
            copy_editor_agent,
        ],
        additional_authorized_imports=["re"],
        # system_prompt="""You are a blog post creation manager. Coordinate between research, writing, and editing teams.
        # Follow these steps:
        # 1. Use research_agent to gather information
        # 2. Pass research to research_checker_agent to check for relevance
        # 3. Pass research to writer_agent to create the initial draft
        # 4. Send draft to editor for final polish
        # 4. Save the final markdown file
        # """
    )

    result = blog_manager.run(f"""Create a blog post about: {topic}
    1. First, research the topic thoroughly, focus on specific products and sources
    2. Then, write an engaging blog post not just a list
    3. Finally, edit and polish the content
    """)

    return result
