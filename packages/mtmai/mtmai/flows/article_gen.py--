"""
工作流： 文章生成
"""

import asyncio
from datetime import timedelta
from textwrap import dedent

from crewai import Agent, Crew, Process, Task
from prefect import get_run_logger, task
from prefect.tasks import task_input_hash
from pydantic import BaseModel

from mtmai.agents.ctx import mtmai_context
from mtmai.agents.tools.tools import get_tools
from mtmai.models.book_gen import (
    BookOutline,
    Chapter,
    WriteOutlineRequest,
    WriteSingleChapterRequest,
)
from mtmai.mtlibs.aiutils import get_json_format_instructions


@task(
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(seconds=60),
    retries=3,
)
async def article_gen_outline(*, req: WriteOutlineRequest) -> BookOutline:
    """生成文章大纲"""
    llm = await mtmai_context.get_crawai_llm()
    logger = get_run_logger()

    researcher_agent = Agent(
        role="Research Agent",
        goal=dedent("""Gather comprehensive information about {topic} that will be used to create an organized and well-structured book outline.
Here is some additional information about the author's desired goal for the book:\n\n {goal}"""),
        backstory=dedent("""You're a seasoned researcher, known for gathering the best sources and understanding the key elements of any topic.
You aim to collect all relevant information so the book outline can be accurate and informative."""),
        tools=get_tools("search_engine"),
        llm=llm,
        verbose=True,
    )
    outliner_agent = Agent(
        role="Book Outlining Agent",
        goal=dedent("""Based on the research, generate a book outline about the following topic: {topic}
The generated outline should include all chapters in sequential order and provide a title and description for each chapter.
Here is some additional information about the author's desired goal for the book:\n\n {goal}"""),
        backstory=dedent("""You are a skilled organizer, great at turning scattered information into a structured format.
Your goal is to create clear, concise chapter outlines with all key topics and subtopics covered."""),
        llm=llm,
        verbose=True,
    )

    research_topic_task = Task(
        description=dedent("""Research the provided topic of {topic} to gather the most important information that will
be useful in creating a book outline. Ensure you focus on high-quality, reliable sources.

Here is some additional information about the author's desired goal for the book:\n\n {goal}
        """),
        expected_output="A set of key points and important information about {topic} that will be used to create the outline.",
        agent=researcher_agent,
    )
    generate_outline_task = Task(
        description=dedent("""Create a book outline with chapters in sequential order based on the research findings.
Ensure that each chapter has a title and a brief description that highlights the topics and subtopics to be covered.
It's important to note that each chapter is only going to be 3,000 words or less.
Also, make sure that you do not duplicate any chapters or topics in the outline.

Here is some additional information about the author's desired goal for the book:\n\n {goal}"""),
        expected_output="An outline of chapters, with titles and descriptions of what each chapter will contain. Maximum of 3 chapters.  \n\n {format_instructions}",
        output_pydantic=BookOutline,
        agent=outliner_agent,
    )
    crew = Crew(
        agents=[researcher_agent, outliner_agent],
        tasks=[research_topic_task, generate_outline_task],
        process=Process.sequential,
        verbose=True,
    )

    inputs = req
    if isinstance(req, BaseModel):
        inputs = req.model_dump()
    inputs["format_instructions"] = get_json_format_instructions(BookOutline)
    output = await crew.kickoff_async(inputs=inputs)

    logger.info(f"format_instructions: {get_json_format_instructions(BookOutline)}")
    if not output:
        raise ValueError(f"大纲生成失败: {req}")
    if not output.pydantic:
        raise ValueError(
            f"大纲生成失败: 原因是 output.pydantic 没有正确的输出格式,原始内容: {output.raw}"
        )
    return output.pydantic


@task(
    cache_key_fn=task_input_hash,
    cache_expiration=timedelta(days=1),
    retries=3,
)
async def write_book_chapter_crew(*, req: WriteSingleChapterRequest):
    """生成文章一个章节"""
    logger = get_run_logger()

    llm = await mtmai_context.get_crawai_llm()

    researcher_agent = Agent(
        role="Research Agent",
        goal=dedent("""Gather comprehensive information about {topic} and {chapter_title} that will be used to enhance the content of the chapter.
Here is some additional information about the author's desired goal for the book and the chapter:\n\n {goal}
Here is the outline description for the chapter:\n\n {chapter_description}"""),
        backstory=dedent("""You are an experienced researcher skilled in finding the most relevant and up-to-date information on any given topic.
Your job is to provide insightful data that supports and enriches the writing process for the chapter."""),
        # tools=[],
        tools=get_tools("search_engine"),
        llm=llm,
    )

    writer_agent = Agent(
        role="Chapter Writer",
        goal=dedent("""Write a well-structured chapter for the book based on the provided chapter title, goal, and outline.
The chapter should be written in markdown format and contain around 3,000 words."""),
        backstory=dedent("""You are an exceptional writer, known for producing engaging, well-researched, and informative content.
You excel at transforming complex ideas into readable and well-organized chapters."""),
        llm=llm,
    )

    research_chapter_task = Task(
        description=dedent("""Research the provided chapter topic, title, and outline to gather additional content that will be helpful in writing the chapter.
Ensure you focus on reliable, high-quality sources of information.

Here is some additional information about the author's desired goal for the book and the chapter:\n\n {goal}
Here is the outline description for the chapter:\n\n {chapter_description}

When researching, consider the following key points:
- you need to gather enough information to write a 3,000-word chapter
- The chapter you are researching needs to fit in well with the rest of the chapters in the book.

Here is the outline of the entire book:\n\n
{book_outlines}"""),
        expected_output="A set of additional insights and information that can be used in writing the chapter.",
        agent=researcher_agent,
    )

    write_chapter_task = Task(
        description=dedent("""Write a well-structured chapter based on the chapter title, goal, and outline description.
Each chapter should be written in markdown and should contain around 3,000 words.

Here is the topic for the book: {topic}
Here is the title of the chapter: {chapter_title}
Here is the outline description for the chapter:\n\n {chapter_description}

Important notes:
- The chapter you are writing needs to fit in well with the rest of the chapters in the book.

Here is the outline of the entire book:\n\n
{book_outlines}"""),
        agent=writer_agent,
        expected_output="A markdown-formatted chapter of around 3,000 words that covers the provided chapter title and outline description. \n\n {format_instructions}",
        output_pydantic=Chapter,
    )
    crew = Crew(
        agents=[researcher_agent, writer_agent],
        tasks=[research_chapter_task, write_chapter_task],
        process=Process.sequential,
        verbose=True,
    )
    inputs = req.model_dump()
    inputs["format_instructions"] = get_json_format_instructions(Chapter)
    output = await crew.kickoff_async(inputs=inputs)
    if not output:
        raise ValueError(f"章节生成失败: {req}")
    if not output.pydantic:
        raise ValueError(
            f"章节生成失败,原因是 output.pydantic 没有正确的输出格式,原始内容: \n========\n{output.raw}\n========\n"
        )
    return output.pydantic


@task(cache_key_fn=task_input_hash, cache_expiration=timedelta(days=1))
async def write_section(topic):
    logger = get_run_logger()
    logger.info(f"开始写内容:{topic}")
    await asyncio.sleep(5)
    logger.info(f"写内容完成:{topic}")

    return f"Content for {topic}"


class ArticleGenStateRequest(BaseModel):
    topic: str | None = None
    user_id: str | None = None
    site_id: str | None = None
