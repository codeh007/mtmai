from typing import Literal

import structlog
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import StreamingResponse
from openai.types.chat.chat_completion_message_param import ChatCompletionMessageParam
from openai.types.chat.completion_create_params import CompletionCreateParamsBase
from opentelemetry import trace
from pydantic import BaseModel

# from mtmai.agents.chat_profiles.profiles import get_chat_agent
# from mtmai.agents.ctx import init_mtmai_http_context, mtmai_context
# from mtmai.agents.graphs.hello_graph import HelloGraph
# from mtmai.agents.opencanvas.opencanvas_graph import OpenCanvasGraph
# from mtmai.agents.sitegen_graph.sitegen_graph import SiteGenGraph
# from mtmai.assistants.assistants import get_assistant_agent
from mtmai.deps import OptionalUserDep
from mtmai.llm.llm import (
    call_chat_completions,
    chat_completions_stream_generator,
    default_llm_model,
)

router = APIRouter()
LOG = structlog.get_logger()

tracer = trace.get_tracer_provider().get_tracer(__name__)


API_KEY_NAME = "Authorization"


class MtmaiCompletionRequest(CompletionCreateParamsBase):
    class Config:
        arbitrary_types_allowed = True

    chatId: bool | None = False
    threadId: str | None = None
    isChat: bool | None = False
    messages: list[ChatCompletionMessageParam] | None = []
    model: str | None = None
    stream: bool | None = False


default_chat_profile = "taskrunner"


async def context_sse_stream():
    while True:
        message = await mtmai_context.get_next_event()
        if message:
            yield f"data: {message}\n\n"  # Format the message for SSE


@router.post("/chat/completions")
async def chat_completions(
    request: Request,
    user: OptionalUserDep,
):
    """以兼容 openai completions 协议的方式 反代其他 ai 提供商的 completions api"""
    request_data = await request.json()

    prompt = request_data.get("prompt")
    if prompt:
        request_data["messages"] = [
            {
                "role": "user",
                "content": prompt,
            }
        ]
        request_data.pop("prompt")

    is_stream = request_data.get("stream")

    model = request_data.get("model") or default_llm_model
    is_chat = request.headers.get("X-Chat") == "1" or request_data.get("isChat")

    init_mtmai_http_context(
        thread_id=request_data.get("threadId"),
        user_id=str(user.id) if user else None,
    )
    is_pull = request_data.get("isPull")

    if is_pull:
        await mtmai_context.init_mq()
        return StreamingResponse(
            mtmai_context.mq.pull_messages(),
            media_type="text/event-stream",
        )

    request_data["model"] = model
    messages = request_data.get("messages")
    if not is_chat:
        # open ai 兼容的模型调用
        if not messages:
            return HTTPException(status_code=503, detail="No messages provided")
        if is_stream:
            return StreamingResponse(
                chat_completions_stream_generator(request_data),
                media_type="text/event-stream",
            )

        else:
            return await call_chat_completions(request_data)

    params = request_data.get("params")
    chat_profile = request_data.get("chatProfile", default_chat_profile)
    if chat_profile == "hello_graph":
        hello_graph = HelloGraph()
        return StreamingResponse(
            hello_graph.run_graph(
                messages=messages,  # user_id=str(user.id), params=params
            ),
            media_type="text/event-stream",
        )
    if chat_profile == "opencanvas":  # 未完成
        hello_graph = OpenCanvasGraph()
        return StreamingResponse(
            hello_graph.run_graph(
                messages=messages,  # user_id=str(user.id), params=params
                user_id=str(user.id) if user else None,
                params=params,
            ),
            media_type="text/event-stream",
        )
    if chat_profile == "sitegen":
        graph = SiteGenGraph()
        return StreamingResponse(
            graph.run_graph(
                messages=messages,  # user_id=str(user.id), params=params
                user_id=str(user.id) if user else None,
                params=params,
            ),
            media_type="text/event-stream",
        )

    if chat_profile == "taskrunner":
        graph_app = await get_chat_agent("taskrunner")

        graph_app.onRequest(messages=messages, inputs={})
        # 这里不用返回数据，因为现在使用 redis 消息队列。内部会自动向队列发送消息。
        # return StreamingResponse(
        #     context_sse_stream,
        #     media_type="text/event-stream",
        # )

    else:
        assistant_agent = await get_assistant_agent(chat_profile)
        return StreamingResponse(
            assistant_agent.stream_messages(
                messages=messages, user_id=str(user.id), params=params
            ),
            media_type="text/event-stream",
            headers={
                # "x-vercel-ai-data-stream": "v1",
                "Content-Type": "text/plain; charset=utf-8",
                "Vary": "RSC, Next-Router-State-Tree, Next-Router-Prefetch",
                "Cache-Control": "no-store, no-cache, must-revalidate, proxy-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
                "Surrogate-control": "no-store",
            },
        )


class ChatEventRequest(BaseModel):
    thread_id: str


class ChatEventItem(BaseModel):
    role: Literal["user", "assistant"]
    content: str


class ChatEventResponse(BaseModel):
    items: list[ChatEventItem]


# import os
# from shutil import rmtree

# import torch
# from fastapi import APIRouter, Request
# from langchain_huggingface.embeddings import HuggingFaceEmbeddings
# from optimum.onnxruntime import ORTModelForFeatureExtraction
# from pydantic import BaseModel, Field
# from starlette.concurrency import run_in_threadpool
# from transformers import AutoTokenizer

# from mtmai.mtlibs.logging import get_logger

# router = APIRouter()

# logger = logging.getLogger()
# tokenizer = None
# model_current = None
# device = None
# provider = None


# class CreateEmbeddingRequest(BaseModel):
#     input: str | list[str] = Field(description="The input to embed.")
#     model: str | None
#     # input_type: Optional[str]  # 可能没用
#     encoding_format: str | None


# class Embedding(BaseModel):
#     embedding: list[float] = Field(max_length=2048)


# class CreateEmbeddingResponse(BaseModel):
#     data: list[Embedding]


# def save_model(model_name, _device, _reload=False):
#     global device, provider
#     device = _device
#     provider = "CUDAExecutionProvider" if device == "cuda" else "CPUExecutionProvider"
#     optimize = "O4" if device == "cuda" else "O3"
#     ort_model_output = f".vol/model_auto_opt_{optimize}"
#     model_exists = os.path.exists(ort_model_output) and os.path.exists(
#         ort_model_output + "/config.json"
#     )
#     if (model_exists and _reload) or not model_exists:
#         if model_exists:
#             rmtree(ort_model_output)
#         print(f"Loading {model_name} model and exporting it to ONNX..")
#         _model = ORTModelForFeatureExtraction.from_pretrained(
#             model_name, provider=provider, export=True, cache_dir="/tmp"
#         )
#         _model.save_pretrained(ort_model_output)
#     elif model_exists and not _reload:
#         print(f"Model {model_name} already exists! use RELOAD=True to reload")
#     return "./" + ort_model_output


# def load_model(model_name, _device, _reload):
#     global tokenizer, model_current
#     ort_model_output = save_model(model_name, _device, _reload=_reload)
#     print(f"Loading {model_name} model from {ort_model_output}..")
#     tokenizer = AutoTokenizer.from_pretrained(ort_model_output)
#     model_current = ORTModelForFeatureExtraction.from_pretrained(
#         ort_model_output, provider=provider
#     )


# def _create_embedding(input: str | list[str], model: str, encoding_format: str | None):
#     global tokenizer
#     if not isinstance(input, list):
#         input = [input]

#     if not model_current:
#         print("加载模型", model)
#         load_model(model, "cpu", False)
#     encoded_input = tokenizer(
#         input, padding=True, truncation=True, return_tensors="pt"
#     ).to(device)

#     # 使用 torch 属于比较底层的操作。
#     with torch.no_grad():
#         sentence_embeddings = model_current(**encoded_input)[0][:, 0]
#     sentence_embeddings = (
#         torch.nn.functional.normalize(sentence_embeddings, p=2, dim=1).cpu().numpy()
#     )
#     data = [Embedding(embedding=embedding) for embedding in sentence_embeddings]
#     return CreateEmbeddingResponse(data=data)
#     # 也可以使用 高级库，例如：
#     # embModel = getEmbdingModel()
#     # texts = [input]
#     # nums=embModel.embed_documents(texts)


# @router.post(
#     "/v1/embeddings",
#     #  response_model=CreateEmbeddingResponse,
# )
# async def create_embedding(
#     # request: CreateEmbeddingRequest,
#     request: Request,
# ):
#     """
#     供前端获取计算 embdings （目前使用本地模型）
#     api 接口可以参考： https://platform.openai.com/docs/guides/embeddings/what-are-embeddings
#     """
#     # print("v1 embeddings 调用:", request.model)
#     aa = await request.json()
#     print(aa)
#     return await run_in_threadpool(_create_embedding, **aa)


# embdingModel = None


# def getEmbdingModel():
#     """
#     文档： 嵌入模型排行榜 https://huggingface.co/spaces/mteb/leaderboard
#     """
#     global embdingModel
#     if embdingModel is None:
#         # model_name = "mixedbread-ai/mxbai-embed-large-v1"
#         # model_name = "bert-base-uncased" #维度768，# 体积约0.5G
#         # model_name = "microsoft/Phi-3-mini-4k-instruct" # 维度 3072 模型文件约8G，性能上的消耗比较大。模型加载时长约20s
#         # model_name = "iampanda/zpoint_large_embedding_zh" # 中文 维度：1792
#         # model_name = "voyageai/voyage-lite-02-instruct" # 1536
#         model_name = "infgrad/stella-large-zh-v2"  # 1024
#         hf_embeddings = HuggingFaceEmbeddings(
#             model_name=model_name,
#             # trust_remote_code=True
#         )
#         embdingModel = hf_embeddings
#     return embdingModel
