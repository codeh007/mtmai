import json
import logging
import pprint
import time
from collections.abc import AsyncIterator, Generator

from fastapi.encoders import jsonable_encoder
from fastapi.responses import StreamingResponse
from json_repair import repair_json
from langchain_core.messages import BaseMessage
from langchain_core.output_parsers import PydanticOutputParser
from openai import Stream
from openai.types.chat.chat_completion_chunk import (
    ChatCompletionChunk,
    Choice,
    ChoiceDelta,
)
from opentelemetry import trace
from pydantic import BaseModel

from mtmai.mtlibs import mtutils

logger = logging.getLogger()
tracer = trace.get_tracer_provider().get_tracer(__name__)


def repaire_json(json_like_input: str):
    good_json_string = repair_json(json_like_input, skip_json_loads=True)
    return good_json_string


def chat_complations_stream_text(response: Stream[ChatCompletionChunk]):
    """
    兼容 vercel ai sdk
    等同于 nextjs /api/chat/route.ts 中的:
        return await streamText({
            model: getAiModalDefault(),
            messages,
        }).toDataStreamResponse();
    """
    for chunk in response:
        if not chunk.choices[0].finish_reason:
            if chunk.choices[0].delta.content:
                yield f'{chunk.choices[0].index}: "{chunk.choices[0].delta.content}"\n'
                # yield f"data: {json.dumps(chunk2)}\n"
        else:
            # 结束
            final_chunk = {
                "id": chunk.id,
                "object": chunk.object,
                "created": chunk.created,
                "model": chunk.model,
                "finishReason": chunk.choices[0].finish_reason,
                "usage": jsonable_encoder(chunk.usage),
            }
            yield f"d: {json.dumps(final_chunk)}\n"
            # 明确的结束符
            yield "[DONE]\n"


def stream_response(stream_chunck: Stream[ChatCompletionChunk]):
    def gen_stream():
        for chunk in stream_chunck:
            pprint.pp(chunk)
            yield f"data: {json.dumps(jsonable_encoder( chunk))}\n\n"
            if chunk.choices[0].finish_reason is not None:
                yield "data: [DONE]\n"

    return StreamingResponse(gen_stream(), media_type="text/event-stream")


async def stream_text(stream: AsyncIterator[BaseMessage]):
    async for ai_message_chunk in stream:
        if ai_message_chunk.content:
            yield f"0:{json.dumps(ai_message_chunk.content)} \n"


def gen_text_stream(words: Generator[str, None]):
    """以stream 的方式向chat 输出字符串 (旧代码)"""
    for w in words:
        chat_chunk = ChatCompletionChunk(
            id=mtutils.gen_orm_id_key(),
            object="chat.completion.chunk",
            created=int(time.time()),
            model="agent",
            choices=[
                Choice(
                    index=0,
                    delta=ChoiceDelta(content=w, role="assistant", text=w),
                )
            ],
        )
        yield f"data: {json.dumps(jsonable_encoder(chat_chunk))}\n\n"


class ClientAttachment(BaseModel):
    name: str
    contentType: str
    url: str


class ToolInvocation(BaseModel):
    toolCallId: str
    toolName: str
    args: dict
    result: dict


class ClientMessage(BaseModel):
    role: str
    content: str
    experimental_attachments: list[ClientAttachment] | None = None
    toolInvocations: list[ToolInvocation] | None = None


class ClientAttachment(BaseModel):
    name: str
    contentType: str
    url: str


class ToolInvocation(BaseModel):
    toolCallId: str
    toolName: str
    args: dict
    result: dict


def gen_text_stream_2(words: Generator[str, None]):
    """(可能是旧代码)以stream 的方式向chat 输出字符串"""
    for w in words:
        chat_chunk = ChatCompletionChunk(
            id=mtutils.gen_orm_id_key(),
            object="chat.completion.chunk",
            created=int(time.time()),
            model="agent",
            choices=[
                Choice(
                    index=0,
                    delta=ChoiceDelta(content=w, role="assistant", text=w),
                )
            ],
        )
        yield f"data: {json.dumps(jsonable_encoder(chat_chunk))}\n\n"

    # 发送结束标志
    end_chunk = ChatCompletionChunk(
        id=mtutils.gen_orm_id_key(),
        object="chat.completion.chunk",
        created=int(time.time()),
        model="agent",
        choices=[
            Choice(
                index=0,
                delta=ChoiceDelta(content="", role="assistant"),
                finish_reason="stop",
            )
        ],
    )
    yield f"data: {json.dumps(jsonable_encoder(end_chunk))}\n\n"


def convert_to_openai_messages(messages: list[ClientMessage]):
    openai_messages = []

    for message in messages:
        parts = []

        parts.append({"type": "text", "text": message.content})

        if message.experimental_attachments:
            for attachment in message.experimental_attachments:
                if attachment.contentType.startswith("image"):
                    parts.append(
                        {"type": "image_url", "image_url": {"url": attachment.url}}
                    )

                elif attachment.contentType.startswith("text"):
                    parts.append({"type": "text", "text": attachment.url})

        if message.toolInvocations:
            tool_calls = [
                {
                    "id": tool_invocation.toolCallId,
                    "type": "function",
                    "function": {
                        "name": tool_invocation.toolName,
                        "arguments": json.dumps(tool_invocation.args),
                    },
                }
                for tool_invocation in message.toolInvocations
            ]

            openai_messages.append({"role": "assistant", "tool_calls": tool_calls})

            tool_results = [
                {
                    "role": "tool",
                    "content": json.dumps(tool_invocation.result),
                    "tool_call_id": tool_invocation.toolCallId,
                }
                for tool_invocation in message.toolInvocations
            ]

            openai_messages.extend(tool_results)

            continue

        openai_messages.append({"role": message.role, "content": parts})

    return openai_messages


def get_json_format_instructions(pydantic_model: BaseModel):
    """
    从pydantic 模型中获取 json 格式的格式化说明,(使用了增强提示词)
    """
    parser = PydanticOutputParser(pydantic_object=pydantic_model)
    format_instructions = parser.get_format_instructions()
    format_instructions = (
        format_instructions
        + "\n\nDouble-check your output to ensure it is valid JSON before submitting.\n"
    )
    return format_instructions
