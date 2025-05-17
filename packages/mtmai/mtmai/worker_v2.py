"""
基于 pgmq 消息队列的 worker 入口
"""

import asyncio
import json
import logging
from typing import Optional

from google.genai import types  # noqa: F401
from loguru import logger
from smolagents import CodeAgent
from smolagents.memory import ActionStep, FinalAnswerStep, PlanningStep
from sqlalchemy import text
from sqlalchemy.exc import ArgumentError

from mtmai.core.config import settings
from mtmai.db.db import get_async_session
from mtmai.model_client import get_default_smolagents_model


class WorkerV2:
  def __init__(
    self,
    *,
    db_url: str,
  ) -> None:
    self.db_url = db_url
    self._running = False
    self._task: Optional[asyncio.Task] = None
    try:
      # db_engine = create_engine(db_url)
      # self.db_engine: Engine = db_engine
      pass
    except Exception as e:
      if isinstance(e, ArgumentError):
        raise ValueError(f"Invalid database URL format or argument '{db_url}'.") from e
      if isinstance(e, ImportError):
        raise ValueError(f"Database related module not found for URL '{db_url}'.") from e
      raise ValueError(f"Failed to create database engine for URL '{db_url}'") from e

  async def start(self) -> None:
    """
    启动 worker
    """
    if self._running:
      logger.warning("Worker is already running")
      return

    logging.info(f"Starting worker for queue: {settings.QUEUE_SHORTVIDEO_COMBINE}")
    self._running = True
    self._task = asyncio.create_task(self._consume_messages())

  async def start_block(self) -> None:
    """
    阻塞启动 worker
    """
    await self.start()
    await self._consume_messages()

  async def _get_one_message(self):
    """
    获取一条消息
    """
    async with get_async_session() as session:
      result_data = (
        await session.exec(
          text("SELECT * FROM taskmq_pull(:worker_id, :task_type)"),
          params={"worker_id": "aa", "task_type": "bb"},
        )
      ).all()
      await session.commit()
      return result_data

  async def _post_task_result(self, msg_id: str, task_id: str, task_result: any, error: str | None = None) -> None:
    """
    确认消息
    """
    async with get_async_session() as session:
      await session.exec(
        text("SELECT taskmq_submit_result(:msg_id, :task_id, :result,:error)"),
        params={
          "msg_id": msg_id,
          "task_id": task_id,
          "result": json.dumps(task_result),
          "error": error,
        },
      )
      await session.commit()
    logger.info(f"_post_task_result 完成, {task_id}")

  async def _consume_messages(self) -> None:
    """
    消费消息的主循环
    """
    wait_seconds = 5
    while self._running:
      try:
        result_data = await self._get_one_message()
        if len(result_data) == 0:
          await asyncio.sleep(1)
          continue

        for msg_tuple in result_data:
          msg_id = msg_tuple.msg_id
          message_obj = msg_tuple.message
          task_id = message_obj.get("task_id")
          if not task_id:
            raise ValueError("task_id 为空")
          payload = message_obj.get("input")
          if not payload:
            raise ValueError("input 为空")
          if isinstance(payload, str):
            payload = json.loads(payload)
          try:
            result = await self.on_message(msg_id, task_id, payload)
            await self._post_task_result(msg_id, task_id, result)
          except Exception as e:
            logger.exception(e)
            await self._post_task_result(msg_id, task_id, None, str(e))
            await asyncio.sleep(1)
            continue

      except Exception as e:
        if "Connection timed out" in str(e) or "could not receive data from server" in str(e):
          logger.warning(f"数据库连接超时,将在{wait_seconds}秒后重试: {e}")
          await asyncio.sleep(wait_seconds)
          continue
        logger.error(f"消费消息错误: {e}")
        await asyncio.sleep(2)
        continue

  async def stop(self) -> None:
    """
    停止 worker
    """
    if not self._running:
      logger.warning("Worker is not running")
      return

    logging.info(f"Stopping worker for queue: {self.queue_name}")
    self._running = False

    if self._task:
      self._task.cancel()
      try:
        await self._task
      except asyncio.CancelledError:
        pass
      self._task = None

  async def on_message(self, msg_id: str, task_id: str, payload: dict):
    """
    处理消息
    """
    logger.info(f"on_message\t{msg_id}\t{task_id}\t{payload}")
    input_obj = payload.get("input")
    if not input_obj:
      raise ValueError("input 为空")
    task_type = payload.get("task_type")

    task_result = None
    match task_type:
      case "smolagent":
        task_result = await self.on_run_small_agent(task_id, payload)
      case "mtmagent":
        task_result = await self.on_run_mtmagent(task_id, payload)
      case _:
        raise ValueError(f"不支持的任务类型: {task_type}")
    # if task_result:
    #     await self._post_task_result(task_id, task_result)
    return task_result

  async def on_run_small_agent(self, task_id: str, payload: dict) -> None:
    """
    处理消息
    """
    logger.info(f"on_message\t{task_id}\t{payload}")
    input_task = payload.get("input")
    code_agent = CodeAgent(
      model=get_default_smolagents_model(),
      # tools=[visualizer, TextInspectorTool(self.model, self.text_limit)],
      tools=[],
      max_steps=25,
      verbosity_level=2,
      additional_authorized_imports=["*"],
      planning_interval=4,
      managed_agents=[],
    )

    final_answer = None
    for step in code_agent.run(task=input_task, stream=True, reset=True):
      if isinstance(step, ActionStep):
        pass
      if isinstance(step, PlanningStep):
        pass
      if isinstance(step, FinalAnswerStep):
        final_answer = step.final_answer
    return final_answer

  async def on_run_mtmagent(self, task_id: str, payload: dict) -> None:
    """
    处理消息
    """
    from mtmai.agents.mtmagent import MtmaiAgent

    asyncio.run(MtmaiAgent().run())
