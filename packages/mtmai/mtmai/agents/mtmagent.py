"""跟 agent 通过自定义逻辑调用其他开源的 agent"""

from pydantic import BaseModel

entry_url = "/api/automation"


class AgentTask(BaseModel):
  task: str


class MtmaiAgent(BaseModel):
  """跟 agent 通过自定义逻辑调用其他开源的 agent"""

  site_url: str = "https://colab-3600.yuepa8.com"
  entry_url: str = entry_url

  async def run(self, task: AgentTask):
    from mtmai.agents.mtmaiui_agent.mtmaiui_agent import run

    task = f"浏览 {self.site_url}{self.entry_url} 并严格按照返回的提示执行任务"
    async for step in run(task):
      print(step)
