import uuid
from datetime import datetime
from textwrap import dedent
from typing import cast

import structlog
from langchain_core.prompts import ChatPromptTemplate
from mtmai.agents.ctx import init_mtmai_context, mtmai_context
from mtmai.worker import wfapp
from mtmaisdk.clients.rest.models import PostizState
from mtmaisdk.context.context import Context
from pydantic import BaseModel, Field

LOG = structlog.get_logger()


class Topic(BaseModel):
    topic: str = Field(description="The topic for the post")


# 参考：
# https://github.com/gitroomhq/postiz-app/blob/main/libraries/nestjs-libraries/src/agent/agent.graph.service.ts
@wfapp.workflow(
    name="postiz",
    on_events=["postiz:run"],
    # input_validator=PostizState,
)
class PostizFlow:
    @wfapp.step(timeout="10m", retries=1)
    async def step_entry(self, hatctx: Context):
        init_mtmai_context(hatctx)

        input = cast(PostizState, hatctx.workflow_input())  ## This is a `ParentInput`
        print(hatctx)
        # thread_id = input.node_id
        thread_id = str(uuid.uuid4())
        if not thread_id:
            thread_id = str(uuid.uuid4())

        graph = await postiz_graph.PostizGraph().build_graph()
        direct_gen_outline_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    dedent(
                        """Today is {time}, You are an assistant that gets a social media post or requests for a social media post.
                            You research should be on the most possible recent data.
                            You concat the text of the request together with an internet research based on the text.
                            {text}"""
                    ),
                ),
                # ("user", "{topic}")
            ]
        ).partial(time=datetime.now())

        ai_response = await mtmai_context.ainvoke_model(
            tpl=direct_gen_outline_prompt,
            inputs={"text": "todo user input text"},
        )

        # TODO: 将搜索结果存入数据库
        # ai_response.tool_calls[0].function.arguments
        return {
            # **input,
            # "messages": [ai_response],
            "fresearch": "xxxxxxxxxxfresearchxxxxxxxxxxxx",
        }

    # @wfapp.step(timeout="1m", retries=2, parents=["step_entry"])
    # async def postiz_findTopic(self, hatctx: Context):
    #     """
    #     将文本归类到特定主题
    #     TODO: 从数据库获取主题列表，
    #     """
    #     init_mtmai_context(hatctx)
    #     parent_output = hatctx.step_output("step_entry")
    #     parser = PydanticOutputParser(pydantic_object=Topic)
    #     # const allTopics = await this._postsService.findAllExistingTopicsOfCategory(
    #     # state?.category!
    #     # );
    #     # if (allTopics.length === 0) {
    #     # return { topic: null };
    #     # }
    #     step_entry_result = hatctx.step_output("step_entry")
    #     llm = await mtmai_context.get_llm_openai(llm_config_name="chat")
    #     structured_llm = llm.with_structured_output(Topic)

    #     result = (
    #         ChatPromptTemplate.from_template(
    #             """
    #         You are an assistant that gets a text that will be later summarized into a social media post
    #         and classify it to one of the following topics: {topics}
    #         text: {text}
    #     """
    #         )
    #         .pipe(structured_llm)
    #         .invoke(
    #             {
    #                 "topics": "todo topics",
    #                 "text": parent_output.get("fresearch", ""),
    #             }
    #         )
    #     )

    #     # content = hatctx.state.messages.filter((f) => f instanceof ToolMessage);
    #     # return { fresearch: content };
    #     return {"result": result}
