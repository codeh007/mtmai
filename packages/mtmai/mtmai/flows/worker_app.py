from __future__ import annotations

import asyncio
import sys

from loguru import logger
from mtmai import loader
from mtmai.core.config import settings
from mtmai.hatchet import Hatchet

from .flow_ag import FlowAg

mtmapp = None


async def run_worker():
    global mtmapp
    maxRetry = settings.WORKER_MAX_RETRY
    for i in range(maxRetry):
        try:
            mtmapp = Hatchet.from_config(
                loader.ConfigLoader().load_client_config(
                    loader.ClientConfig(
                        server_url=settings.GOMTM_URL,
                        # 绑定 python 默认logger,这样,就可以不用依赖 hatchet 内置的ctx.log()
                        # logger=logger,
                    )
                ),
                debug=True,
            )
            await mtmapp.boot()

            worker = mtmapp.worker(settings.WORKER_NAME)
            # await setup_hatchet_workflows(mtmapp, worker)
            worker.register_workflow(FlowAg())
            # worker.register_workflow(FlowBrowser())

            logger.info("connect gomtm server success")
            break

        except Exception as e:
            if i == maxRetry - 1:
                sys.exit(1)
            logger.info(f"failed to connect gomtm server, retry {i + 1},err:{e}")
            # raise e
            await asyncio.sleep(settings.WORKER_INTERVAL)
    # 非阻塞启动(注意: eventloop, 如果嵌套了,可能会莫名其妙的退出)
    # self.worker.setup_loop(asyncio.new_event_loop())
    # asyncio.create_task(self.worker.async_start())
    # 阻塞启动
    await worker.async_start()


# async def setup_hatchet_workflows(wfapp: Hatchet, worker: Worker):
#     class MyResultType(TypedDict):
#         my_func: str

#     @wfapp.function(
#         name="my_func2232",
#     )
#     def my_func(context: Context) -> MyResultType:
#         return MyResultType(my_func="testing123")

#     # @workflow(
#     #     name="ag",
#     #     on_events=["ag:run"],
#     #     input_validator=AgentRunInput,
#     # )
#     # class FlowAg:
#     #     @step(timeout="60m")
#     #     async def step_entry(self, hatctx: Context):
#     #         input = cast(AgentRunInput, hatctx.workflow_input())
#     #         if not input.run_id:
#     #             input.run_id = hatctx.workflow_run_id()
#     #         if not input.step_run_id:
#     #             input.step_run_id = hatctx.step_run_id

#     #         # agent_rpc_client = AgentRpcClient(self.config.server_url)
#     #         runtime = GrpcWorkerAgentRuntime(agent_rpc_client=wfapp.client.ag)
#     #         worker_team = WorkerTeam(client=wfapp.client)
#     #         task_result = await worker_team.handle_message(input)
#     #         return {
#     #             "ok": True,
#             }

#     worker.register_workflow(FlowAg())


# async def setup_browser_workflows(wfapp: Hatchet, worker: Worker):
#     @wfapp.workflow(
#         on_events=["browser:run"],
#         # input_validator=CrewAIParams,
#     )
#     class FlowBrowser:
#         @wfapp.step(timeout="10m", retries=1)
#         async def run(self, hatctx: Context):
#             from mtmai.clients.rest.models import BrowserParams

#             # from mtmai.agents.browser_agent import BrowserAgent

#             input = BrowserParams.model_validate(hatctx.workflow_input())
#             # init_mtmai_context(hatctx)

#             # ctx = get_mtmai_context()
#             # tenant_id = ctx.tenant_id
#             # llm_config = await wfapp.rest.aio.llm_api.llm_get(
#             #     tenant=tenant_id, slug="default"
#             # )
#             # llm = ChatOpenAI(
#             #     model=llm_config.model,
#             #     api_key=llm_config.api_key,
#             #     base_url=llm_config.base_url,
#             #     temperature=0,
#             #     max_tokens=40960,
#             #     verbose=True,
#             #     http_client=httpx.Client(transport=LoggingTransport()),
#             #     http_async_client=httpx.AsyncClient(transport=LoggingTransport()),
#             # )

#             # 简单测试llm 是否配置正确
#             # aa=llm.invoke(["Hello, how are you?"])
#             # print(aa)
#             # agent = BrowserAgent(
#             #     generate_gif=False,
#             #     use_vision=False,
#             #     tool_call_in_content=False,
#             #     # task="Navigate to 'https://en.wikipedia.org/wiki/Internet' and scroll down by one page - then scroll up by 100 pixels - then scroll down by 100 pixels - then scroll down by 10000 pixels.",
#             #     task="Navigate to 'https://en.wikipedia.org/wiki/Internet' and to the string 'The vast majority of computer'",
#             #     llm=llm,
#             #     browser=Browser(config=BrowserConfig(headless=False)),
#             # )
#             # await agent.run()
