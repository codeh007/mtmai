from textwrap import dedent

from crewai import Agent, Crew, Process, Task
from pydantic import BaseModel

# from mtmai.agents.ctx import mtmai_context
from mtmai.agents.tools.tools import get_tools
from mtmai.models.book_gen import BookOutline


async def call_crew(
    crew: Crew, input: dict | BaseModel, pydanticOutput: None | BaseModel = None
):
    if isinstance(input, BaseModel):
        input = input.model_dump()
    output = await crew.kickoff_async(inputs=input)

    if not output:
        raise ValueError("调用 crew 失败，因输出内容是空的")
    if not output.pydantic:
        # output.pydantic = GenBlogTopicsOutput.model_validate_json(
        #     repaire_json(output.raw)
        # )
        # if BaseModel:
        #     try:
        #         output.pydantic = BaseModel.model_validate_json(
        #             repaire_json(output.raw)
        #         )
        #     except Exception:
        #         raise Exception(f"call_crew 解释 JSON 出错, json: {output.raw}")
        return output.raw
    if not output.pydantic:
        raise ValueError(
            f"调用 crew 失败，llm输出不是 json 格式: \n========\n{output.raw}\n========\n"
        )
    if pydanticOutput:
        return pydanticOutput.model_validate(output.pydantic)
    return output.pydantic.model_dump()


async def crew_gen_outline(callback) -> BookOutline:
    """生成文章大纲"""
    llm = await mtmai_context.get_crawai_llm()
    researcher_agent = Agent(
        role="Research Agent",
        goal=dedent("""Gather comprehensive information about {topic} that will be used to create an organized and well-structured book outline.
Here is some additional information about the author's desired goal for the book:\n\n {goal}"""),
        backstory=dedent("""You're a seasoned researcher, known for gathering the best sources and understanding the key elements of any topic.
You aim to collect all relevant information so the book outline can be accurate and informative."""),
        tools=get_tools("search_engine"),
        llm=llm,
        verbose=True,
        max_retry_limit=100,
        max_rpm=60,
        step_callback=callback,
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
        step_callback=callback,
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
        step_callback=callback,
        task_callback=callback,
    )
    return crew


class GenBlogTopicsOutput(BaseModel):
    topics: list[str] = "主题列表，按优先级更好的方前面"
