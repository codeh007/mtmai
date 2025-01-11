import json
import re
import uuid

import orjson
from json_repair import repair_json
from langchain_core.messages import AIMessage, ToolCall
from langgraph.checkpoint.memory import MemorySaver

from mtmai.llm.llm import get_llm_chatbot_default

memory = MemorySaver()


async def call_model(
    prompt: list,
    model: str,
    max_retries: int = 2,
    response_format: str | None = None,
    api_key: str | None = None,
) -> str:
    """
    这个函数原本 仅能使用 chatgpt 模型，并且要求返回格式必须是 json
    现在暂时用 from together import Together 替代。
    """
    optional_params = {}
    if response_format == "json":
        optional_params = {"response_format": {"type": "json_object"}}

    # search = TavilySearchResults(max_results=2)
    tools = []
    # agent_executor = create_react_agent(
    #     model,
    #     # tools,
    #     checkpointer=memory,
    # )
    llm = get_llm_chatbot_default()
    response = await llm.ainvoke(prompt)
    # print(response)
    response.content
    return response.content

    # llmget_llm_chatbot_default()
    # lc_messages = convert_openai_messages(prompt)

    # llm = lcllm_openai_chat()
    # response = (
    #     # ChatOpenAI(
    #     #     model=model,
    #     #     max_retries=max_retries,
    #     #     model_kwargs=optional_params,
    #     #     api_key=api_key,
    #     # )
    #     llm.invoke(lc_messages).content
    # )
    # together = Together()
    # extract = together.chat.completions.create(
    #     messages=prompt,
    #     model="meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo",
    #     # response_format=optional_params,
    #     response_format={
    #         "type": "json_object",
    #         # "schema": VoiceNote.model_json_schema(),
    #     },
    # )

    # extract_json = extract_json_from_string(extract.choices[0].message.content)
    # return extract_json
    # output = json.loads(extract.choices[0].message.content)
    # print(json.dumps(output, indent=2))
    # return output


def extract_json_from_string(json_str: str) -> dict:
    # 清理 JSON 字符串
    cleaned_json_str = clean_json_string(json_str)
    if cleaned_json_str.startswith("{"):
        return cleaned_json_str
    match = re.search(r"```.*?({[\s\S]*?})\s*```", cleaned_json_str)
    if match:
        json_str = match.group(1)
        return json_str
    print(f"未找到 JSON 数据 : {cleaned_json_str}")
    return None


def clean_json_string(json_str: str) -> str:
    # 替换非法控制字符
    json_str = re.sub(r"[\x00-\x1f\x7f]", "", json_str)
    return json_str


def fix_tool_calls(ai_msg: AIMessage):
    if not ai_msg.content or (
        ai_msg.tool_calls and ai_msg.tool_calls[0].type == "tool_call"
    ):
        # 已是正确格式
        return ai_msg
    # 情况1： 以lamma3.1 常见的 <function> 格式回复函数函数调用
    function_regex = r"<function=(\w+)>(.*?)</function>"
    match = re.search(function_regex, ai_msg.content, re.DOTALL)
    if match:
        function_name, args_string = match.groups()

        args = json.loads(args_string)
        ai_msg.tool_calls.append(
            ToolCall(
                name=function_name,
                arguments=args,
                id=str(uuid.uuid4()),
                type="tool_call",
            )
        )
        ai_msg.content = ""
        return ai_msg

    # 情况2 函数调用没有出现在 tool_calls 字段，而是出现在 content 中，json格式
    # 例子： {"name": "ToDevelopAssistant", "parameters": {"request": "I want to edit an article"}}
    loaded_data = orjson.loads(repair_json(ai_msg.content))
    if (
        isinstance(loaded_data, dict)
        and "name" in loaded_data
        and "parameters" in loaded_data
    ):
        ai_msg.tool_calls.append(
            ToolCall(
                name=loaded_data["name"],
                arguments=loaded_data["parameters"],
                id=str(uuid.uuid4()),
                type="tool_call",
            )
        )
        ai_msg.content = ""
        return ai_msg
    return ai_msg
