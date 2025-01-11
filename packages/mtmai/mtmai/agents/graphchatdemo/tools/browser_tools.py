import json
import logging

import requests
from crewai import Agent, Crew, Task
from langchain.tools import tool
from unstructured.partition.html import partition_html

# from mtmai.mtlibs.aiutils import lcllm_openai_chat
from mtmai.llm.llm import get_llm_chatbot_default

logger = logging.getLogger()


class BrowserTools:
    @tool("Scrape website content")
    async def scrape_and_summarize_website(website):
        """Useful to scrape and summarize a website content"""
        # url = f"https://chrome.browserless.io/content?token={os.environ['BROWSERLESS_API_KEY']}"
        url = "http://172.17.0.1:13001"

        logger.info('调用工具 BrowserTools.scrape_and_summarize_website: "%s"', website)

        payload = json.dumps({"url": website})
        headers = {"cache-control": "no-cache", "content-type": "application/json"}
        response = requests.request(
            "POST", url, headers=headers, data=payload, timeout=30
        )
        elements = partition_html(text=response.text)
        content = "\n\n".join([str(el) for el in elements])
        content = [content[i : i + 8000] for i in range(0, len(content), 8000)]
        summaries = []

        llm = get_llm_chatbot_default()
        for chunk in content:
            agent = Agent(
                role="Principal Researcher",
                goal="Do amazing researches and summaries based on the content you are working with",
                backstory="You're a Principal Researcher at a big company and you need to do a research about a given topic.",
                allow_delegation=False,
                llm=llm,
            )
            task = Task(
                agent=agent,
                description=f"Analyze and summarize the content bellow, make sure to include the most relevant information in the summary, return only the summary nothing else.\n\nCONTENT\n----------\n{chunk}",
                expected_output="A bullet list summary of the top 5 most important AI news",  # 需要正确设置
            )
            # summary = task.execute()
            # Execute the crew
            crew = Crew(agents=[agent], tasks=[task], verbose=2)
            result = crew.kickoff()

            summaries.append(task.output.summary)
        return "\n\n".join(summaries)
