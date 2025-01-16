import openai


def call_model_together(messages=None):
    client = openai.OpenAI(
        base_url="https://api.together.xyz/v1",
        # base_url="https://3400-niutrans-classicalmoder-9fbkp8wozlh.ws-us116.gitpod.io/api/llm_proxy",
        api_key="29cead0a87a33dff3d5f5d377adb962fcf5d0661770d3994fc6d0e95c70c5139",
    )

    tools = [
        {
            "type": "function",
            "function": {
                "name": "get_current_weather",
                "description": "Get the current weather in a given location",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "location": {
                            "type": "string",
                            "description": "The city and state, e.g. San Francisco, CA",
                        },
                        # "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]},
                    },
                },
            },
        }
    ]

    messages = messages or [
        {
            "role": "system",
            # "content": "You are a helpful assistant that can access external functions. The responses from these function calls will be appended to this dialogue. Please provide responses based on the information from these function calls.",
            "content": "You are a helpful assistant that can access external functions.",
        },
        {
            "role": "user",
            "content": "What is the current temperature of New York, San Francisco and Chicago?",
        },
    ]

    response = client.chat.completions.create(
        # model="mistralai/Mixtral-8x7B-Instruct-v0.1",
        model="meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo",
        messages=messages,
        tools=tools,
        # tool_choice="auto",
        # max_tokens=8000, # 注意事项，together ai，是可以调用工具的，但是如果有max_tokens 参数，就会调用不成功，仅仅返回普通的对话消息。
        n=1,
        # stream=False,
        # temperature=0.7,
    )
    return response
