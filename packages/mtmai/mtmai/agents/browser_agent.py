import json
from typing import Any, Optional, Type, TypeVar

from browser_use import Agent, AgentHistoryList
from browser_use.agent.views import (ActionResult, AgentError, AgentHistory,
                                     AgentHistoryList, AgentOutput,
                                     AgentStepInfo)
from browser_use.browser.browser import Browser, BrowserConfig
from browser_use.utils import time_execution_async
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage, SystemMessage
from langchain_openai import ChatOpenAI
from matplotlib import hatch
from mtmaisdk.clients.rest.models import BrowserParams
from mtmaisdk.context.context import Context

from mtmai.agents.ctx import get_mtmai_context, init_mtmai_context
from mtmai.mtlibs.httpx_transport import LoggingTransport
from mtmai.worker import wfapp


class BrowserAgent(Agent):
    pass
    # @time_execution_async('--get_next_action')
    # async def get_next_action(self, input_messages: list[BaseMessage]) -> AgentOutput:
    #     """Get next action from LLM based on current state"""

    #     # structured_llm = self.llm.with_structured_output(self.AgentOutput, include_raw=True)
    #     # response: dict[str, Any] = await structured_llm.ainvoke(input_messages)  # type: ignore  # noqa: F821
        
    #     content = AgentOutput.model_json_schema()
    #     systemToolPrompt = SystemMessage(content=f"VERY IMPORTANT: YOU MUST FOLLOW THE STRUCTURE OF THE JSON SCHEMA: \n{content}")
    #     input_messages.append(systemToolPrompt)
    #     response: AIMessage = await self.llm.ainvoke(input_messages)  # type: ignore
        
    #     json_data = json.loads(response.content)
    #     parsed = AgentOutput.model_validate(json_data)
    #     # parsed: AgentOutput = response['parsed']
    #     if parsed is None:
    #         raise ValueError('Could not parse response.')

    #     # cut the number of actions to max_actions_per_step
    #     parsed.action = parsed.action[: self.max_actions_per_step]
    #     self._log_response(parsed)
    #     self.n_steps += 1

    #     return parsed