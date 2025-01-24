import logging
import uuid
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import HTTPException
from sqlmodel import delete, desc, select
from sqlmodel.ext.asyncio.session import AsyncSession

from mtmai.db.db import get_async_session
from mtmai.models.chat import ChatElement, ChatFeedback, ChatStep, ChatThread

logger = logging.getLogger()


async def get_user_threads(
    session: AsyncSession,
    user_id: str,
    thread_id: str = None,
    limit: int = 100,
    skip: int = 0,
) -> Optional[list[dict]]:
    """
    获取用户的 chat threads , 包含 steps 和 feedbacks
    """
    query = (
        select(ChatThread)
        .where((ChatThread.userId == user_id) | (ChatThread.id == thread_id))
        .order_by(desc(ChatThread.created_at))
        .limit(limit)
        .offset(skip)
    )

    result = await session.exec(query)
    user_threads = result.scalars().all()

    if not user_threads:
        return None

    thread_ids = [thread.id for thread in user_threads]

    steps_feedbacks_query = (
        select(ChatStep, ChatFeedback)
        .join(ChatFeedback, ChatStep.id == ChatFeedback.for_id, isouter=True)
        .where(ChatStep.thread_id.in_(thread_ids))
        .order_by(ChatStep.created_at)
    )

    steps_feedbacks_result = await session.exec(steps_feedbacks_query)
    steps_feedbacks = steps_feedbacks_result.all()

    threads_dict = []

    # convert to chainlit  user_threads format
    for thread in user_threads:
        thread_dict = {
            "id": str(thread.id),
            "createdAt": thread.created_at.isoformat(),
            "name": thread.name,
            "userId": str(thread.userId),
            "userIdentifier": thread.userIdentifier,
            "tags": thread.tags,
            "metadata": thread.meta,
            "steps": [],
        }

        for step, feedback in steps_feedbacks:
            if str(step.thread_id) == str(thread.id):
                step_dict = {
                    "id": str(step.id),
                    "name": step.name,
                    "type": step.type,
                    "threadId": str(step.thread_id) if step.thread_id else None,
                    "parentId": str(step.parent_id) if step.parent_id else None,
                    "streaming": step.streaming,
                    "waitForAnswer": step.wait_for_answer,
                    "isError": step.is_error,
                    "metadata": step.meta,
                    "tags": step.tags,
                    "input": step.input,
                    "output": step.output,
                    "createdAt": step.created_at.isoformat(),
                    "start": step.start.isoformat() if step.start else None,
                    "end": step.end.isoformat() if step.end else None,
                    "generation": step.generation,
                    "showInput": step.show_input,
                    "language": step.language,
                    "indent": step.indent,
                    "feedback": {
                        "value": feedback.value if feedback else None,
                        "comment": feedback.comment if feedback else None,
                    },
                }
                thread_dict["steps"].append(step_dict)

        threads_dict.append(thread_dict)

    return threads_dict


async def get_steps_by_thread(thread_id: uuid.UUID | str):
    if isinstance(thread_id, str):
        thread_id = uuid.UUID(thread_id)
    async with get_async_session() as session:
        query = select(ChatStep).where(ChatStep.thread_id == thread_id)
        result = await session.exec(query)
        return result.all()


async def create_chat_element(
    chat_element_dict: dict,
    user_id: str | None = None,
):
    async with get_async_session() as session:
        new_item = ChatElement.model_validate(chat_element_dict)
        if not new_item.mime:
            new_item.mime = "application/octet-stream"
        session.add(new_item)
        await session.commit()
        return new_item


async def get_chat_element(
    thread_id: uuid.UUID | str,
    element_id: uuid.UUID | str,
):
    if isinstance(thread_id, str):
        thread_id = uuid.UUID(thread_id)
    if isinstance(element_id, str):
        element_id = uuid.UUID(element_id)

    async with get_async_session() as session:
        query = select(ChatElement).where(
            ChatElement.threadId == thread_id, ChatElement.id == element_id
        )
        result = await session.exec(query)
        return result.first()


async def is_thread_author(username: str, thread_id: str):
    thread_author = await get_thread_author(thread_id)

    if not thread_author:
        raise HTTPException(status_code=404, detail="Thread not found")

    if thread_author != str(username):
        raise HTTPException(status_code=401, detail="Unauthorized")
    else:
        return True


async def create_thread(
    *,
    thread_id: uuid.UUID | None = None,
    userId: str,
    meta_data: dict = None,
    tags: list[str] = [],
    name: str = None,
):
    _name = name or f"chat-{datetime.now().strftime('%m%d-%H-%M')}"

    async with get_async_session() as session:
        new_thread = ChatThread(
            id=thread_id,
            userIdentifier=str(userId),
            meta=meta_data or {},
            tags=tags or [],
            userId=userId,
            name=_name,
        )
        session.add(new_thread)
        await session.commit()
        await session.refresh(new_thread)
        return new_thread


async def update_thread(
    *,
    thread_id: uuid.UUID | str,
    name: Optional[str] = None,
    userId: uuid.UUID | str = None,
    metadata: Optional[Dict] = None,
    tags: Optional[List[str]] = None,
):
    if isinstance(thread_id, str):
        thread_id = uuid.UUID(thread_id)
    if isinstance(userId, str):
        userId = uuid.UUID(userId)

    async with get_async_session() as session:
        existing_thread = await get_thread(thread_id)
        if existing_thread is None:
            existing_thread = await create_thread(
                thread_id=thread_id,
                userId=userId,
                meta_data=metadata,
                tags=tags or [],
                name=name,
            )
        if name is not None:
            existing_thread.name = name
        if userId is not None:
            existing_thread.userIdentifier = str(userId)
            existing_thread.userId = userId
        if metadata is not None:
            existing_thread.meta = metadata
        if tags is not None:
            existing_thread.tags = tags
        await session.commit()


async def get_thread(thread_id: uuid.UUID | str):
    if isinstance(thread_id, str):
        thread_id = uuid.UUID(thread_id)

    async with get_async_session() as session:
        query = select(ChatThread).where(ChatThread.id == thread_id)
        result = await session.exec(query)
        return result.one_or_none()


async def get_thread_author(thread_id: uuid.UUID | str):
    result = await get_thread(thread_id)
    if result:
        return result.userIdentifier
    else:
        return None


async def delete_thread(thread_id: uuid.UUID | str):
    # Delete feedbacks/elements/steps/thread
    if isinstance(thread_id, str):
        thread_id = uuid.UUID(thread_id)

    async with get_async_session() as session:
        await session.exec(
            delete(ChatFeedback).where(ChatFeedback.thread_id == thread_id)
        )
        await session.exec(
            delete(ChatElement).where(ChatElement.thread_id == thread_id)
        )
        await session.exec(delete(ChatStep).where(ChatStep.thread_id == thread_id))
        await session.exec(delete(ChatThread).where(ChatThread.id == thread_id))
        await session.commit()
