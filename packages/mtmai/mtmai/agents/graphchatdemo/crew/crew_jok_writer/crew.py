from crewai import Crew
from langchain_core.runnables import Runnable

from mtmai.llm.llm import get_llm_chatbot_default

from .agents import JokAgents
from .tasks import MyTasks


class JokeCrew:
    def __init__(self, runnable: Runnable):
        agents = JokAgents()
        # self.filter_agent = agents.email_filter_agent()
        self.joke_writer_agent = agents.joke_writer_agent()
        # self.writer_agent = agents.email_response_writer()
        self.runnable = runnable

    async def kickoff(self, state):
        tasks = MyTasks()
        # emails = ["a@a.com"]
        llm = get_llm_chatbot_default()
        crew = Crew(
            agents=[
                self.joke_writer_agent,
                # self.action_agent,
                # self.writer_agent,
            ],
            tasks=[
                tasks.task_demo_human(self.joke_writer_agent),
                # tasks.action_required_emails_task(self.action_agent),
                # tasks.draft_responses_task(self.writer_agent),
            ],
            verbose=True,
            manager_llm=llm,
            function_calling_llm=llm,
            planning_llm=llm,
        )
        result = await crew.kickoff_async()

        artifact = (
            {
                "artiface_type": "Document",
                "title": "任务结果",
                "props": {"title": "任务结果", "content": result},
            },
        )
        return {**state, "artifacts": [artifact]}
