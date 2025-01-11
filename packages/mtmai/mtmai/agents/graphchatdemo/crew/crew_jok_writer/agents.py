import logging
from textwrap import dedent

from crewai import Agent

from mtmai.llm.llm import get_llm_chatbot_default

logger = logging.getLogger()


def step_callback(a):
    logger.info("调用 step_callback %s", a)


class JokAgents:
    def __init__(self):
        pass

    def joke_writer_agent(self):
        llm = get_llm_chatbot_default()

        return Agent(
            role="幽默段子写手",
            goal="创作幽默段子",
            backstory=dedent("""\
				作为一个网站的博主,你非常删除编写适合短视频社交平台的幽默段子， 作品容易吸引年轻人浏览，点击关注"""),
            verbose=True,
            allow_delegation=False,
            llm=llm,
            step_callback=step_callback,
        )

    # def email_action_agent(self):
    #     return Agent(
    #         role="Email Action Specialist",
    #         goal="Identify action-required emails and compile a list of their IDs",
    #         backstory=dedent("""\


# 			With a keen eye for detail and a knack for understanding context, you specialize
# 			in identifying emails that require immediate action. Your skill set includes interpreting
# 			the urgency and importance of an email based on its content and context."""),
#         tools=[
#             # GmailGetThread(api_resource=self.gmail.api_resource),
#             # TavilySearchResults(),
#         ],
#         verbose=True,
#         allow_delegation=False,
#     )

# def email_response_writer(self):
#     return Agent(
#         role="Email Response Writer",
#         goal="Draft responses to action-required emails",
#         backstory=dedent("""\
# 			You are a skilled writer, adept at crafting clear, concise, and effective email responses.
# 			Your strength lies in your ability to communicate effectively, ensuring that each response is
# 			tailored to address the specific needs and context of the email."""),
#         tools=[
#             # TavilySearchResults(),
#             # GmailGetThread(api_resource=self.gmail.api_resource),
#             CreateDraftTool.create_draft,
#         ],
#         verbose=True,
#         allow_delegation=False,
#     )
