from __future__ import annotations

from mtmai.context.context import Context
from mtmai.hatchet import step, workflow


@workflow(
    on_events=["browser:run"],
    # input_validator=CrewAIParams,
)
class FlowBrowser:
    @step(timeout="10m", retries=1)
    async def run(self, hatctx: Context):
        from mtmai.clients.rest.models import BrowserParams

        # from mtmai.agents.browser_agent import BrowserAgent

        input = BrowserParams.model_validate(hatctx.workflow_input())
        # init_mtmai_context(hatctx)

        # ctx = get_mtmai_context()
        # tenant_id = ctx.tenant_id
        # llm_config = await wfapp.rest.aio.llm_api.llm_get(
        #     tenant=tenant_id, slug="default"
        # )
        # llm = ChatOpenAI(
        #     model=llm_config.model,
        #     api_key=llm_config.api_key,
        #     base_url=llm_config.base_url,
        #     temperature=0,
        #     max_tokens=40960,
        #     verbose=True,
        #     http_client=httpx.Client(transport=LoggingTransport()),
        #     http_async_client=httpx.AsyncClient(transport=LoggingTransport()),
        # )

        # 简单测试llm 是否配置正确
        # aa=llm.invoke(["Hello, how are you?"])
        # print(aa)
        # agent = BrowserAgent(
        #     generate_gif=False,
        #     use_vision=False,
        #     tool_call_in_content=False,
        #     # task="Navigate to 'https://en.wikipedia.org/wiki/Internet' and scroll down by one page - then scroll up by 100 pixels - then scroll down by 100 pixels - then scroll down by 10000 pixels.",
        #     task="Navigate to 'https://en.wikipedia.org/wiki/Internet' and to the string 'The vast majority of computer'",
        #     llm=llm,
        #     browser=Browser(config=BrowserConfig(headless=False)),
        # )
        # await agent.run()
