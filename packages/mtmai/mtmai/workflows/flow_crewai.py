import asyncio

import litellm
from crewai import Agent, Crew, Process, Task
from fastapi.encoders import jsonable_encoder
# from mtmai.workflows.step_base import get_wf_log_callbacks
from mtmaisdk.clients.rest.models import CrewAIParams
from mtmaisdk.clients.rest.models.call_agent import CallAgent
from mtmaisdk.context.context import Context

from mtmai.worker import wfapp
from mtmai.workflows.crews import call_crew


@wfapp.workflow(
    on_events=["crewai:call"],
    input_validator=CrewAIParams,
)
class FlowCrewAIAgent:
    @wfapp.step(timeout="10m", retries=1)
    async def run(self, hatctx: Context):
        input = CallAgent.model_validate(hatctx.workflow_input())
        # callback = get_wf_log_callbacks(hatctx)
        # llm = get_llm(input.llm, callback)
        agents = []
        agent_dict = {}
        for agent in input.agents:
            new_agent = Agent(
                role=agent.role,
                backstory=agent.backstory,
                goal=agent.goal,
                llm=llm,
                verbose=True,
                max_retry_limit=100,
                max_rpm=60,
                step_callback=callback,
                task_callback=callback,
                tools=[
                    self.get_tool(self.ctx, "httpfetch"),
                    # self.get_tool(self.ctx, "runnewtask"),
                ],
                memory=True,
            )
            agents.append(new_agent)
            agent_dict[agent.name] = new_agent

        tasks = []

        for task in input.tasks:
            target_agent = agent_dict[task.agent]
            if not target_agent:
                raise ValueError(f"缺少名称为 {task.agent} 的 agent")
            new_task = Task(
                description=task.description,
                expected_output=task.expected_output,
                agent=target_agent,
                callback=callback,
                # output_pydantic=getOuputSchemaByName(task.output_json_schema_name)
                # if task.output_json_schema_name is not None
                # else None,
            )
            tasks.append(new_task)

        crew = Crew(
            agents=agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
            step_callback=callback,
            task_callback=callback,
            memory=True,
            knowledge_sources=[self.get_crew_knownledge()],
            embedder_config={
                "provider": "ollama",
                "config": {"model": "nomic-embed-text:latest"},
            },
        )
        crew.short_term_memory = self.get_crew_short_term_mem(crew)
        crew.long_term_memory = self.get_crew_long_term_mem(crew)
        crew.entity_memory = self.get_crew_entiry_mem(crew)

        try:
            result = jsonable_encoder(await call_crew(crew, input.input))
            if isinstance(result, str):
                # self.ctx.put_stream('0:"hello from crew result"\n')
                self.emit(result)
                return {"raw": result}
            return result
        except litellm.RateLimitError as e:
            await asyncio.sleep(20)
            self.ctx.log("速率限制，休眠")
            raise e
            self.ctx.log("速率限制，休眠")
            raise e
