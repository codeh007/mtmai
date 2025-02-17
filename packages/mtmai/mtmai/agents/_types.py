from typing import Dict

from autogen_agentchat.base import TaskResult
from pydantic import BaseModel


# Define WriterAgent configuration model
class ChatAgentConfig(BaseModel):
    topic_type: str
    description: str
    system_message: str


# Define UI Agent configuration model
class UIAgentConfig(BaseModel):
    topic_type: str
    artificial_stream_delay_seconds: Dict[str, float]

    @property
    def min_delay(self) -> float:
        return self.artificial_stream_delay_seconds.get("min", 0.0)

    @property
    def max_delay(self) -> float:
        return self.artificial_stream_delay_seconds.get("max", 0.0)


class ApiSaveTeamState(BaseModel):
    tenant_id: str
    # team_id: str
    state: dict
    componentId: str
    runId: str


class ApiSaveTeamTaskResult(BaseModel):
    tenant_id: str
    team_id: str
    task_result: TaskResult


class SetupHfSpaceMsg(BaseModel):
    tenant_id: str
    username: str
    password: str


class LogItemMsg(BaseModel):
    content: str


class MsgStartWebServer(BaseModel):
    pass


class MsgGetTeam(BaseModel):
    tenant_id: str
    team_id: str
