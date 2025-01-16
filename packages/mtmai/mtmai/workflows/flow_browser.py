import asyncio
import os
import sys

from browser_use import Agent
from browser_use.browser.browser import Browser, BrowserConfig
from fastapi.encoders import jsonable_encoder
from langchain_openai import ChatOpenAI
from mtmaisdk.clients.rest.models import CrewAIParams
from mtmaisdk.clients.rest.models.call_agent import CallAgent
from mtmaisdk.context.context import Context

from mtmai.worker import wfapp

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))




@wfapp.workflow(
    on_events=["browser:run"],
    # input_validator=CrewAIParams,
)
class FlowBrowser:
    
    def __init__(self):
        print("init FlowBrowser")
    @wfapp.step(timeout="10m", retries=1)
    async def run(self, hatctx: Context):
        input = CallAgent.model_validate(hatctx.workflow_input())
        # llm = hatctx.aio.
        llm_config = await wfapp.rest.aio.llm_api.llm_get()
        
