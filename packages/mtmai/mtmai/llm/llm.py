import json
import logging

import openai
from langchain_openai import ChatOpenAI
from openai import OpenAI
from openai.types.chat.completion_create_params import (
    CompletionCreateParamsNonStreaming,
)
from opentelemetry import trace

from mtmai.core.config import settings

logger = logging.getLogger()
tracer = trace.get_tracer_provider().get_tracer(__name__)


def get_default_openai_client(model_name: str = ""):
    """获取默认的 跟 openai 兼容的 ai 客户端."""
    # provider_name = model.split("/")[0]
    # api_url = get_api_base(provider_name)
    openai_client = None
    # api_key = (
    #     "b135fd4bed9be2a988e0376d1bb0977fcb8b6a88ec9f35da8138fa49eb9a0d50"  # together
    # )
    api_key = settings.GROQ_TOKEN  # _get_api_key(model_name)
    # base_url = _get_api_base(model_name)
    # model = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
    base_url = "https://api.groq.com/openai/v1"
    openai_client = openai.Client(
        base_url=base_url,
        api_key=api_key,
    )
    # return openai_client
    return openai.OpenAI(
        base_url=base_url,
        api_key=api_key,
    )
    # return wrap_openai(openai_client)


# def _get_api_key(model_name: str):
#     # key = random.choice(groq_tokens)
#     # print("api key %s", key)
#     # together_api_key = (
#     #     "10747773f9883cf150558aca1b0dda81af4237916b03d207b8ce645edb40a546"
#     # )
#     # return together_api_key

#     groq_key = settings.GROQ_TOKEN
#     return groq_key


# def get_target_model_name(model_name: str):
#     # if model_name.startswith("groq/"):
#     #     return model_name[5:]
#     # return model_name
#     # return get_default_model_name()

#     # return "llama3-groq-70b-8192-tool-use-preview"
#     return "llama3-groq-8b-8192-tool-use-preview"


# def _get_api_base(model_name: str):
#     # if provider == "groq":
#     #     return "https://api.groq.com/openai/v1"
#     # if provider == "together":
#     #     return "https://api.together.xyz/v1"
#     # if provider == "workerai":
#     #     CLOUDFLARE_ACCOUNT_ID = os.getenv("CLOUDFLARE_ACCOUNT_ID")
#     #     return f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/v1"
#     # raise Exception("未知的provider:" + provider)
#     return "https://api.groq.com/openai/v1"


# def lcllm_openai_chat(model_name: str = ""):
#     """获取 langchain 兼容的 openai chat 对象."""
#     api_key = settings.GROQ_TOKEN  # _get_api_key(model_name)
#     base_url = _get_api_base(model_name)
#     model = get_target_model_name(model_name)
#     return ChatOpenAI(
#         base_url=base_url,
#         api_key=api_key,
#         model=model,
#         temperature=0.1,
#         max_tokens=8000,
#     )


# def get_embeding_llm():
#     api_key = settings.TOGETHER_TOKEN
#     base_url = "https://api.together.xyz/v1"
#     model = "togethercomputer/m2-bert-80M-32k-retrieval"
#     llm_embeding = OpenAIEmbeddings(api_key=api_key, base_url=base_url, model=model)
#     return llm_embeding


def get_llm_tooluse_default():
    api_key = settings.GROQ_TOKEN
    base_url = "https://api.groq.com/openai/v1"
    model = "llama3-groq-8b-8192-tool-use-preview"
    return ChatOpenAI(
        base_url=base_url,
        api_key=api_key,
        model=model,
        temperature=0.1,
        max_tokens=8000,
    )


# default_llm_model = "llama-3.1-8b-instant"
# default_llm_model = "llama-3.1-70b-versatile"
default_llm_model = "llama3-70b-8192"


def get_llm_chatbot_default():
    api_key = settings.GROQ_TOKEN
    base_url = "https://api.groq.com/openai/v1"
    # model = "llama3-groq-8b-8192-tool-use-preview"
    model = default_llm_model
    return ChatOpenAI(
        base_url=base_url,
        api_key=api_key,
        model=model,
        temperature=0.7,
        max_tokens=8000,
    )


def get_llm_long_context_default():
    return get_llm_chatbot_default()


def get_fast_llm():
    return get_llm_chatbot_default()


GROQ_BASE_URL = "https://api.groq.com/openai/v1"


# async def call_chat_completions(request_data: dict):
#     logger.info(f"call_chat_completions: {request_data}")
#     client = OpenAI(api_key=settings.GROQ_TOKEN, base_url=GROQ_BASE_URL)
#     request_data.update({"model": "llama3-groq-8b-8192-tool-use-preview"})

#     completionCreateParamsNonStreaming = CompletionCreateParamsNonStreaming(
#         **request_data
#     )
#     # Remove unexpected keys from the request_data
#     allowed_keys = set(CompletionCreateParamsNonStreaming.__annotations__.keys())
#     filtered_request_data = {k: v for k, v in request_data.items() if k in allowed_keys}

#     completionCreateParamsNonStreaming = CompletionCreateParamsNonStreaming(
#         **filtered_request_data
#     )
#     return client.chat.completions.create(**completionCreateParamsNonStreaming)
# async def call_chat_completions(request_data: dict):
#     logger.info(f"call_chat_completions: {request_data}")
#     client = OpenAI(api_key=settings.GROQ_TOKEN, base_url=GROQ_BASE_URL)
#     request_data["model"] = "llama3-groq-8b-8192-tool-use-preview"

#     # 使用 ** 操作符自动过滤掉不需要的参数
#     return client.chat.completions.create(
#         **CompletionCreateParamsNonStreaming(**request_data).model_dump(exclude_unset=True)
#     )


async def call_chat_completions(request_data: dict):
    logger.info(f"call_chat_completions: {request_data}")
    client = OpenAI(api_key=settings.GROQ_TOKEN, base_url=GROQ_BASE_URL)
    request_data["model"] = "llama3-groq-8b-8192-tool-use-preview"

    # 过滤参数
    allowed_params = CompletionCreateParamsNonStreaming.__annotations__.keys()
    filtered_data = {k: v for k, v in request_data.items() if k in allowed_params}

    return client.chat.completions.create(**filtered_data)


async def chat_completions_stream_generator(
    params: dict,
):
    logger.info(f"call_chat_completions: {params}")

    client = OpenAI(api_key=settings.GROQ_TOKEN, base_url=GROQ_BASE_URL)

    # 过滤参数
    allowed_params = CompletionCreateParamsNonStreaming.__annotations__.keys()
    filtered_data = {k: v for k, v in params.items() if k in allowed_params}
    response = client.chat.completions.create(
        **filtered_data,
    )

    for chunk in response:
        chunk_data = chunk.to_dict()
        yield f"data: {json.dumps(chunk_data)}\n\n"
    yield "data: [DONE]\n\n"


# 根据名字获取 llm, 名字格式： together/xxx 或者 groq/xxx
async def getllm_auto(name: str):
    llm_config_item = get_graph_config().get(name)
    if not llm_config_item:
        raise Exception(f"未找到大语言模型配置: {name}")

    provider = llm_config_item.get("provider")
    if not provider:
        raise Exception(f"未找到大语言模型配置: {name}")

    if provider == "groq":
        base_url = "https://api.groq.com/openai/v1"
    elif provider == "together":
        base_url = "https://api.together.xyz/v1"
    else:
        raise Exception(f"未知的provider: {provider}")

    api_key = llm_config_item.get("api_key")
    model = llm_config_item.get("model")

    chatOpenAi = ChatOpenAI(
        base_url=base_url,
        api_key=api_key,
        model=model,
        temperature=0.7,
        max_tokens=8000,
    )
    return chatOpenAi
