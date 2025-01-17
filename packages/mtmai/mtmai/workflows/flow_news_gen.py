
from typing import Iterator

from mtmaisdk.context.context import Context
from phi.storage.workflow.sqlite import SqlWorkflowStorage
from phi.utils.pprint import pprint_run_response
from phi.workflow import RunResponse

from mtmai.agents.ctx import get_mtmai_context, init_mtmai_context
from mtmai.agents.phiagents.news_report_generator.news_report_generator import (
    GenerateNewsReport,
)
from mtmai.worker import wfapp


@wfapp.workflow(
    on_events=["flow_new_generator:run"],
    # input_validator=CrewAIParams,
)
class FlowNewsGen:
    # 使用 phidata 尝试 自动生成文章. 但是发现这样的问题
    # 1. 对于 多个 Agent 组合,再结合 phidata 自带的工作流, 事实跟直接使用 langgraph 区别不大.
    #    另外, 对于 llm 调用的部分 phi 有自己的封装方式, 不方便用于调试. 特别是对于 429 错误的处理, 程序默认是自动退出的. 
    #    结论是,还不如直接使用langgraph 
    def __init__(self):
        print("init FlowNewGenerator")
    @wfapp.step(timeout="10m", retries=1)
    async def run(self, hatctx: Context):
        # input = BrowserParams.model_validate(hatctx.workflow_input())
        init_mtmai_context(hatctx)
        
        ctx= get_mtmai_context()
        tenant_id =  ctx.tenant_id
        llm_config = await wfapp.rest.aio.llm_api.llm_get(
            tenant=tenant_id,
            slug="default"
        )        
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
        
        
        # The topic to generate a report on
        topic = "IBM Hashicorp Acquisition"

        # Instantiate the workflow
        generate_news_report = GenerateNewsReport(
            llmConfig=llm_config,
            session_id=f"generate-report-on-{topic}",
            storage=SqlWorkflowStorage(
                table_name="generate_news_report_workflows",
                db_file=".vol/news_report_generator/workflows.db",
            ),
        )

        # Run workflow
        report_stream: Iterator[RunResponse] = generate_news_report.run(
            topic=topic, use_search_cache=True, use_scrape_cache=True, use_cached_report=False
        )

        # Print the response
        pprint_run_response(report_stream, markdown=True)

        
        
        
                