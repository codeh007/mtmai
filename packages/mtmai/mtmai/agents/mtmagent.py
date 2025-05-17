"""跟 agent 通过自定义逻辑调用其他开源的 agent"""

from mtmai.db.db import get_async_session
from mtmai.db.models import MtTaskStep
from pydantic import BaseModel
from smolagents import ActionStep, FinalAnswerStep, PlanningStep

entry_url = "/api/automation"


class MtmaiAgent(BaseModel):
  """跟 agent 通过自定义逻辑调用其他开源的 agent"""

  site_url: str = "https://colab-3600.yuepa8.com"
  entry_url: str = entry_url

  async def run(self):
    from mtmai.agents.mtmaiui_agent.mtmaiui_agent import run

    task = f"浏览 {self.site_url}{self.entry_url} 并严格按照返回的提示执行任务"
    async for step in run(task):
      # print(step)
      await self.append_step(step)

  async def append_step(self, step: ActionStep | PlanningStep | FinalAnswerStep):
    """保存 agent 运行的步骤信息(Memory)"""
    async with get_async_session() as session:
      task_step = MtTaskStep(data=step.dict())
      session.add(task_step)
      await session.commit()
      await session.refresh(task_step)
      return task_step
