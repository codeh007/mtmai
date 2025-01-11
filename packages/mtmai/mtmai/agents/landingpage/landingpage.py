import json
import logging
from pathlib import Path

from crewai import Agent, Crew, Task
from fastapi import APIRouter

# from langchain.agents.agent_toolkits import FileManagementToolkit
from pydantic import BaseModel

from mtmai.agents.landingpage.tasks import TaskPrompts
from mtmai.tools.browser_tools import BrowserTools
from mtmai.tools.file_tools import FileTools
from mtmai.tools.search_tools import SearchTools
from mtmai.tools.template_tools import TemplateTools

logger = logging.getLogger()

router = APIRouter()


class LandingPageCrew:
    def __init__(self, idea):
        self.agents_config = json.loads(
            Path("mtmai/agents/landingpage/config/agents.json").read_text()
        )
        self.idea = idea
        self.__create_agents()

    def run(self):
        expanded_idea = self.__expand_idea()
        components = self.__choose_template(expanded_idea)
        self.__update_components(components, expanded_idea)

    def __expand_idea(self):
        expand_idea_task = Task(
            description=TaskPrompts.expand().format(idea=self.idea),
            agent=self.idea_analyst,
            expected_output="",  # 需要正确设置
        )
        refine_idea_task = Task(
            description=TaskPrompts.refine_idea(),
            agent=self.communications_strategist,
            expected_output="",  # 需要正确设置
        )
        crew = Crew(
            agents=[self.idea_analyst, self.communications_strategist],
            tasks=[expand_idea_task, refine_idea_task],
            verbose=True,
        )
        expanded_idea = crew.kickoff()
        return expanded_idea

    def __choose_template(self, expanded_idea):
        choose_template_task = Task(
            description=TaskPrompts.choose_template().format(idea=self.idea),
            agent=self.react_developer,
            expected_output="",  # 需要正确设置
        )
        update_page = Task(
            description=TaskPrompts.update_page().format(idea=self.idea),
            agent=self.react_developer,
            expected_output="",  # 需要正确设置
        )
        crew = Crew(
            agents=[self.react_developer],
            tasks=[choose_template_task, update_page],
            verbose=True,
        )
        components = crew.kickoff()
        return components

    def __update_components(self, components, expanded_idea):
        if not components:
            raise Exception("未能正确生成 component")
            return
        components = components.replace("\n", "").replace(" ", "").replace("```", "")
        components = json.loads(components)
        for component in components:
            file_content = open(f"./.vol/workdir/{component.split('./')[-1]}").read()
            create_content = Task(
                description=TaskPrompts.component_content().format(
                    expanded_idea=expanded_idea,
                    file_content=file_content,
                    component=component,
                    expected_output="",  # 需要正确设置
                ),
                agent=self.content_editor_agent,
            )
            update_component = Task(
                description=TaskPrompts.update_component().format(
                    component=component, file_content=file_content
                ),
                agent=self.react_developer,
                expected_output="",  # 需要正确设置
            )
            qa_component = Task(
                description=TaskPrompts.qa_component().format(component=component),
                agent=self.react_developer,
                expected_output="",  # 需要正确设置
            )
            crew = Crew(
                agents=[self.content_editor_agent, self.react_developer],
                tasks=[create_content, update_component, qa_component],
                verbose=True,
            )
            crew.kickoff()

    def __create_agents(self):
        idea_analyst_config = self.agents_config["senior_idea_analyst"]
        strategist_config = self.agents_config["senior_strategist"]
        developer_config = self.agents_config["senior_react_engineer"]
        editor_config = self.agents_config["senior_content_editor"]

        # toolkit = FileManagementToolkit(
        #     root_dir="workdir", selected_tools=["read_file", "list_directory"]
        # )

        self.idea_analyst = Agent(
            **idea_analyst_config,
            verbose=True,
            tools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_website,
            ],
        )

        self.communications_strategist = Agent(
            **strategist_config,
            verbose=True,
            tools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_website,
            ],
        )

        self.react_developer = Agent(
            **developer_config,
            verbose=True,
            max_iter=5,
            tools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_website,
                TemplateTools.learn_landing_page_options,
                TemplateTools.copy_landing_page_template_to_project_folder,
                FileTools.write_file,
            ],
            # + toolkit.get_tools(),
        )

        self.content_editor_agent = Agent(
            **editor_config,
            tools=[
                SearchTools.search_internet,
                BrowserTools.scrape_and_summarize_website,
            ],
        )


class LangpageInputPublic(BaseModel):
    idea: str


@router.post("/run")
async def langdingpage_hello(input: LangpageInputPublic):
    crew = LandingPageCrew(input.idea)
    crew.run()
    return {"idea": input.idea}


# if __name__ == "__main__":
#     idea = input("# Describe what is your idea:\n\n")

#     if not os.path.exists("./.vol/workdir"):
#         os.mkdir("./.vol/workdir")

#     if len(os.listdir("./templates")) == 0:
#         print(
#             dedent("""
#       !!! NO TEMPLATES FOUND !!!
#       ! YOU MUST FORK THIS BEFORE USING IT !

#       Templates are not included as they are Tailwind templates.
#       Place Tailwind individual template folders in `./templates`,
#       if you have a license you can download them at
#       https://tailwindui.com/templates, their references are at
#       `config/templates.json`.

#       This was not tested this with other templates,
#       prompts in `tasks.py` might require some changes
#       for that to work.

#       !!! STOPPING EXECUTION !!!
#       """)
#         )
#         exit()

#     crew = LandingPageCrew(idea)
#     crew.run()
#     zip_file = "workdir"
#     shutil.make_archive(zip_file, "zip", "workdir")
#     shutil.rmtree("workdir")
#     print("\n\n")
#     print("==========================================")
#     print("DONE!")
#     print(f"You can download the project at ./{zip_file}.zip")
#     print("==========================================")
