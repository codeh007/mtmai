import json
import logging
import re

import fastapi

from mtmai.core.config import settings

router = fastapi.APIRouter()
logger = logging.getLogger()


def register_api_router(app: fastapi.FastAPI):
    app.include_router(router)


@router.get(
    settings.API_V1_STR + "/tools/together_demo",
)
async def tools_together_hello():
    # 学习： 根据 together ai 官方文档 llama3.1 模型不直接支持 tools 调用，
    #       官方使用提示词，并解释content 输出的内容的方式间接实现 函数调用。
    from together import Together

    together = Together(
        api_key="b135fd4bed9be2a988e0376d1bb0977fcb8b6a88ec9f35da8138fa49eb9a0d50"
    )
    weatherTool = {
        "name": "get_current_weather",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "The city and state, e.g. San Francisco, CA",
                },
            },
            "required": ["location"],
        },
    }

    toolPrompt = f"""
    You have access to the following functions:

    Use the function '{weatherTool["name"]}' to '{weatherTool["description"]}':
    {json.dumps(weatherTool)}

    If you choose to call a function ONLY reply in the following format with no prefix or suffix:

    <function=example_function_name>{{\"example_name\": \"example_value\"}}</function>

    Reminder:
    - Function calls MUST follow the specified format, start with <function= and end with </function>
    - Required parameters MUST be specified
    - Only call one function at a time
    - Put the entire function call reply on one line
    - If there is no function call available, answer the question like normal with your current knowledge and do not tell the user about function calls

    """

    messages = [
        {
            "role": "system",
            "content": toolPrompt,
        },
        {
            "role": "user",
            "content": "What is the weather in Tokyo?",
        },
    ]

    response = together.chat.completions.create(
        model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        messages=messages,
        max_tokens=1024,
        temperature=0,
    )

    messages.append(response.choices[0].message)

    def parse_tool_response(response: str):
        function_regex = r"<function=(\w+)>(.*?)</function>"
        match = re.search(function_regex, response)

        if match:
            function_name, args_string = match.groups()
            try:
                args = json.loads(args_string)
                return {  # noqa: TRY300
                    "function": function_name,
                    "arguments": args,
                }
            except json.JSONDecodeError as error:
                print(f"Error parsing function arguments: {error}")
                return None
        return None

    # 解释 llm 的输出
    parsed_response = parse_tool_response(response.choices[0].message.content)
    print(parse_tool_response(response.choices[0].message.content))
    # 输出： {
    # "function": "get_current_weather",
    # "arguments": { "location": "Tokyo, Japan" },
    # }

    return messages
