from calendar import day_name

import structlog
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnableConfig

from mtmai.agents.ctx import mtmai_context  # noqa
from mtmai.models.graph_config import HomeChatState

LOG = structlog.get_logger()



class CreateTaskNode:
    def __init__(self):
        pass

    async def __call__(self, state: HomeChatState, config: RunnableConfig):
        user_id = mtmai_context.user_id
        assistant_prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    """<background_story>
你是很有用的助手，擅长根据用户的一段文字，生成结构化的任务模板
</background_story>
{workbench_prompt}
<system_constraints></system_constraints>

<code_formatting_info>
必须使用JSON输出数据
</code_formatting_info>

<message_formatting_info>
</message_formatting_info>

<examples>
    <example>
        <input>
        我要生成文章
        </input>
        <output>
        {{
            "task_type": "articleGen",
            "task_config": {{
                "title": "文章标题",
                "content": "文章内容"
            }}
        }}
        </output>
    </example>
</examples>
{additional_instructions}
""",
                ),
                ("placeholder", "{messages}"),
            ]
        ).partial(
            # tag_names=day_name,
            # MODIFICATIONS_TAG_NAME=MODIFICATIONS_TAG_NAME,
            # cwd="",
            workbench_prompt="",
            # siteId=params.get("siteId", None),
            userId=user_id,
            additional_instructions="",
        )
        ai_msg = await mtmai_context.ainvoke_model(
            assistant_prompt,
            state,
            # tools=primary_assistant_tools
        )
        return {
            "messages": ai_msg,
            # "next": "human",
        }
