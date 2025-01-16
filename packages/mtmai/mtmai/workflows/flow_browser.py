import asyncio
import logging
import os
import sys

import httpx
from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from fastapi.encoders import jsonable_encoder
from langchain_openai import ChatOpenAI
from mtmaisdk.clients.rest.models import BrowserParams
from mtmaisdk.context.context import Context

from mtmai.agents.ctx import get_mtmai_context, init_mtmai_context
from mtmai.worker import wfapp

# 设置 httpx 的调试日志
logging.getLogger("httpx").setLevel(logging.DEBUG)

# 基础日志配置
logging.basicConfig(level=logging.DEBUG)

@wfapp.workflow(
    on_events=["browser:run"],
    # input_validator=CrewAIParams,
)
class FlowBrowser:
    
    def __init__(self):
        print("init FlowBrowser")
    @wfapp.step(timeout="10m", retries=1)
    async def run(self, hatctx: Context):
        input = BrowserParams.model_validate(hatctx.workflow_input())
        init_mtmai_context(hatctx)
        
        ctx= get_mtmai_context()
        tenant_id =  ctx.tenant_id
        llm_config = await wfapp.rest.aio.llm_api.llm_get(
            tenant=tenant_id,
            slug="default"
        )        
        llm = ChatOpenAI(
            model=llm_config.model, 
            api_key=llm_config.api_key, 
            base_url=llm_config.base_url,
            temperature=0,
            max_tokens=4096,
            # stream=True,
            verbose=True
        )
        
        # 简单测试llm 是否配置正确
        # aa=llm.invoke(["Hello, how are you?"])
        # print(aa)
        agent = Agent(
            generate_gif=False,
            use_vision=False,
            # task="Navigate to 'https://en.wikipedia.org/wiki/Internet' and scroll down by one page - then scroll up by 100 pixels - then scroll down by 100 pixels - then scroll down by 10000 pixels.",
            task="Navigate to 'https://en.wikipedia.org/wiki/Internet' and to the string 'The vast majority of computer'",
            llm=llm,
            browser=Browser(config=BrowserConfig(headless=False)),
            
        )
        await agent.run()
                
                
        
