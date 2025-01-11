from textwrap import dedent

from crewai import Task


class MyTasks:
    def filter_emails_task(self, agent, emails):
        task = Task(
            description=dedent("""\
				创作一个关于小猪的幽默段子
				"""),
            agent=agent,
            expected_output="约100字长度的幽默笑话文章,必须是中文的",
        )
        return task

    def task_demo_human(self, agent):
        return Task(
            description=(
                "Conduct a comprehensive analysis of the latest advancements in AI in 2024. "
                "Identify key trends, breakthrough technologies, and potential industry impacts. "
                "Compile your findings in a detailed report. "
                "Make sure to check with a human if the draft is good before finalizing your answer."
            ),
            expected_output="A comprehensive full report on the latest AI advancements in 2024, leave nothing out, 必须中文输出",
            agent=agent,
            # human_input=True,
        )
