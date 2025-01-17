import asyncio
import json
from typing import Any, Dict, List

import httpx
from crewai import LLM, Crew
from crewai.agents.parser import AgentAction, AgentFinish
from crewai.memory.entity.entity_memory import EntityMemory
from crewai.memory.long_term.long_term_memory import LongTermMemory
from crewai.memory.short_term.short_term_memory import ShortTermMemory
from crewai.memory.storage.interface import Storage
from crewai.tools import tool
from fastapi.encoders import jsonable_encoder
from mem0 import Memory
from mtmai.worker import wfapp
from mtmaisdk.context.context import Context

default_max_rpm = 600


def get_default_mem0_config():
    mem0_config = {
        "user_id": "john2",
        "provider": "pgvector",
        "config": {
            "user": "postgres",
            "password": "postgres",
            "host": "127.0.0.1",
            "port": "15432",
        },
        "embedder": {
            "provider": "huggingface",
            "config": {"model": "multi-qa-MiniLM-L6-cos-v1"},
        },
    }
    return mem0_config


class Mem0Storage(Storage):
    """
    Extends Storage to handle embedding and searching across entities using Mem0.
    """

    def __init__(self, type, mem0_config, crew=None):
        super().__init__()

        if type not in ["user", "short_term", "long_term", "entities"]:
            raise ValueError("Invalid type for Mem0Storage. Must be 'user' or 'agent'.")

        self.memory_type = type
        self.crew = crew
        # User ID is required for user memory type "user" since it's used as a unique identifier for the user.
        user_id = self._get_user_id()
        if type == "user" and not user_id:
            raise ValueError("User ID is required for user memory type")

        # stepctx.log(f"Mem0Storage 初始化, {user_id}, {self.memory_type}")

        self.memory = Memory()

    def _sanitize_role(self, role: str) -> str:
        """
        Sanitizes agent roles to ensure valid directory names.
        """
        return role.replace("\n", "").replace(" ", "_").replace("/", "_")

    def save(self, value: Any, metadata: Dict[str, Any]) -> None:
        user_id = self._get_user_id()
        agent_name = self._get_agent_name()
        if self.memory_type == "user":
            self.memory.add(value, user_id=user_id, metadata={**metadata})
        elif self.memory_type == "short_term":
            agent_name = self._get_agent_name()
            self.memory.add(
                value, agent_id=agent_name, metadata={"type": "short_term", **metadata}
            )
        elif self.memory_type == "long_term":
            agent_name = self._get_agent_name()
            self.memory.add(
                value,
                agent_id=agent_name,
                infer=False,
                metadata={"type": "long_term", **metadata},
            )
        elif self.memory_type == "entities":
            entity_name = None
            self.memory.add(
                value, user_id=entity_name, metadata={"type": "entity", **metadata}
            )

    def search(
        self,
        query: str,
        limit: int = 3,
        score_threshold: float = 0.35,
        metadata=None,
    ) -> List[Any]:
        params = {"query": query, "limit": limit}
        if self.memory_type == "user":
            user_id = self._get_user_id()
            params["user_id"] = user_id
        elif self.memory_type == "short_term":
            agent_name = self._get_agent_name()
            params["agent_id"] = agent_name
            params["metadata"] = {"type": "short_term"}
        elif self.memory_type == "long_term":
            agent_name = self._get_agent_name()
            params["agent_id"] = agent_name
            params["metadata"] = {"type": "long_term"}
        elif self.memory_type == "entities":
            agent_name = self._get_agent_name()
            params["agent_id"] = agent_name
            params["metadata"] = {"type": "entity"}

        # Discard the filters for now since we create the filters
        # automatically when the crew is created.
        # 因使用 开源版的 mem0 组件, search不支持 meta 参数
        params.pop("metadata", None)
        results = self.memory.search(**params)
        result = [r for r in results if r["score"] >= score_threshold]
        # stepctx.log(f"获取记忆结果, {result}")
        return result

    def _get_user_id(self):
        if self.memory_type == "user":
            if hasattr(self, "memory_config") and self.memory_config is not None:
                return self.memory_config.get("config", {}).get("user_id")
            else:
                return None
        return None

    def _get_agent_name(self):
        agents = self.crew.agents if self.crew else []
        agents = [self._sanitize_role(agent.role) for agent in agents]
        agents = "_".join(agents)
        return agents


class MtShortTermMem(ShortTermMemory):
    def __init__(self, crew=None, embedder_config=None, storage=None):
        storage = Mem0Storage(
            type="short_term", mem0_config=get_default_mem0_config(), crew=crew
        )
        self.storage = storage


class MtLongTermMemory(LongTermMemory):
    def __init__(self, crew=None, embedder_config=None, storage=None):
        storage = Mem0Storage(
            type="long_term", mem0_config=get_default_mem0_config(), crew=crew
        )
        self.storage = storage


class MtEntityMemory(EntityMemory):
    def __init__(self, crew=None, embedder_config=None, storage=None):
        storage = Mem0Storage(
            type="entities", mem0_config=get_default_mem0_config(), crew=crew
        )
        self.storage = storage


def get_wf_log_callbacks(hatctx: Context):
    def mycallback(data: AgentAction | AgentFinish | dict):
        if isinstance(data, AgentAction):
            hatctx.log(f"AgentAction {data.text}")
        else:
            # print("其他回调信息类型", data)
            hatctx.log(f"其他回调信息类型:\n {jsonable_encoder( data)}")

    return mycallback


@tool("RunNewTask")
def call_spawn_workflow(name: str):
    """用于启动新的任务"""
    wfapp.event.push("task:blog:main", {"test": "test"})


async def do_http_fetch(method: str, url: str):
    async with httpx.AsyncClient() as client:
        response = await client.request(method, url)
        return response.text


@tool("HttpFetch")
def http_fetch(method: str, url: str):
    """http web fetch"""
    try:
        return asyncio.run(do_http_fetch(method, url))
    except Exception as e:
        return f"""http fetch tool error: {e}"""


class MtFlowBase:
    def getLlm(self, hatctx: Context):
        callback = get_wf_log_callbacks(hatctx)
        return LLM(
            model="openai/llama3.1-70b",
            # temperature=llm_item.temperature or None,
            base_url="https://llama3-1-70b.lepton.run/api/v1/",
            api_key="iByWYsIUIBe6qRYBswhLVPRyiVKkYb8r",
            num_retries=5,
            logger_fn=callback,
        )

    def get_tool(self, ctx: Context, tool_name: str):
        if tool_name.lower() == "httpfetch":
            return self.http_fetch_tool(ctx)
        # if tool_name.lower() == "runnewtask":
        #     return self.run_new_task_tool(ctx)
        raise ValueError(f"No tool named {tool_name} found.")

    def http_fetch_tool(self, ctx: Context):
        return http_fetch

    # def run_new_task_tool(self, ctx: Context):
    #     @tool("RunNewTask")
    #     def run_new_task(task_name: str):
    #         """用于启动新的任务"""
    #         try:
    #             do_run_task(ctx, task_name)
    #         except Exception as e:
    #             return f"""run_new_task ERROR: {e}"""

    #     return run_new_task

    def get_crew_short_term_mem(self, crew: Crew):
        return MtShortTermMem(crew=crew)

    def get_crew_long_term_mem(self, crew: Crew):
        return MtLongTermMemory(crew=crew)

    def get_crew_entiry_mem(self, crew: Crew):
        return MtEntityMemory(crew=crew)

    def get_crew_knownledge(self):
        from crewai.knowledge.source.string_knowledge_source import (
            StringKnowledgeSource,
        )

        # 知识库例子：
        string_source = StringKnowledgeSource(
            content="Users name is John. He is 30 years old and lives in San Francisco.",
            metadata={"preference": "personal"},
        )
        return string_source

    def emit(self, event: any):
        if isinstance(event, str):
            json_str = json.dumps(event)
            self.ctx.put_stream(f"0:{json_str}\n")
            self.ctx.put_stream(f"0:{json_str}\n")
            self.ctx.put_stream(f"0:{json_str}\n")
