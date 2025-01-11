import json

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig
from mtmaisdk.clients.rest.models import AssisantState

from mtmai.agents.ctx import mtmai_context


class JokeWriterNode:
    def __init__(self):
        pass

    def node_name(self):
        return "joke_writer"

    async def __call__(self, state: AssisantState, config: RunnableConfig):
        # topic = state.topic
        self.state = state

        # if not topic:
        #     return {
        #         "error": "topic required",
        #     }

        write_joke_result = await self.write_joke_article("hello-topic")

        return {
            # **state,
            "messages": [
                AIMessage(
                    content=json.dumps(write_joke_result),
                )
            ],
        }

    async def write_joke_article(self, topic: str):
        """初始化大纲"""
        # ctx = get_mtmai_ctx()
        # parser = PydanticOutputParser(pydantic_object=Outline)
        direct_gen_outline_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    "You are a witty and humorous joke generator. Please create a joke based on the given topic. The joke should be amusing and elicit laughter. "
                    "[ IMPORTANT ]:"
                    "\n- 必须使用简体中文"
                    "\n- Content length should be suitable for mobile device screens"
                    "\n- The joke should be witty and humorous, provoking laughter"
                    "\n- The content should be positive and uplifting, avoiding vulgarity"
                    "\n- The joke should be wholesome, free from violence, sexual content, or other inappropriate themes"
                    "\n- Ensure the joke is family-friendly and suitable for all audiences",
                ),
                ("user", "{topic}"),
            ]
        )
        ai_response = await mtmai_context.ainvoke_model(
            tpl=direct_gen_outline_prompt,
            inputs={"topic": topic},
        )
        return {
            "joke_content": "test",
        }
