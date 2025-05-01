import asyncio
import os
from dataclasses import dataclass
from textwrap import dedent
from typing import Any, AsyncGenerator, Dict

from browser_use import Agent as BrowseruseAgent
from browser_use import BrowserContextConfig
from browser_use.agent.views import AgentHistoryList
from browser_use.browser.context import BrowserContext as BrowseruseBrowserContext
from google.adk.agents import Agent, BaseAgent
from google.adk.agents.callback_context import CallbackContext
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event, EventActions
from google.adk.tools import BaseTool, ToolContext
from google.genai import types  # noqa
from langchain_google_genai import ChatGoogleGenerativeAI
from loguru import logger
from mtmai.core.config import settings
from mtmai.model_client.utils import get_default_litellm_model
from mtmai.mtlibs.browser_utils.browser_manager import BrowseruseHelper
from playwright.async_api import BrowserContext as PlaywrightBrowserContext
from pydantic import SecretStr
from typing_extensions import override


# ============ Configuration Section ============
@dataclass
class TwitterConfig:
    """Configuration for Twitter posting"""

    openai_api_key: str
    chrome_path: str
    target_user: str  # Twitter handle without @
    message: str
    reply_url: str
    headless: bool = False
    model: str = "gpt-4o-mini"
    base_url: str = "https://x.com/home"


# Customize these settings
config = TwitterConfig(
    openai_api_key=os.getenv("OPENAI_API_KEY"),
    chrome_path="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",  # This is for MacOS (Chrome)
    target_user="XXXXX",
    message="XXXXX",
    reply_url="XXXXX",
    headless=False,
)


# class HelloModel1(BaseModel):
#     name: str
#     age: int


def before_agent_callback(callback_context: CallbackContext):
    """
    在 agent 执行前, 设置获取或者初始化浏览器配置
    """
    agent_name = callback_context.agent_name
    # invocation_id = callback_context.invocation_id
    # print(f"[Callback] Entering agent: {agent_name} (Invocation: {invocation_id})")

    # Example: Check a condition in state
    if callback_context.state.get("skip_agent", False):
        print(f"[Callback] Condition met: Skipping agent {agent_name}.")
        # Return Content to skip the agent's run
        return types.Content(
            parts=[types.Part(text=f"Agent {agent_name} was skipped by callback.")]
        )
    else:
        print(f"[Callback] Condition not met: Proceeding with agent {agent_name}.")
        # Return None to allow the agent's run to execute

        # callback_context.state.update(
        #     {
        #         "browser_config": {
        #             "browser_type": "chrome",
        #             "browser_path": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        #         }
        #     }
        # )
        state_changes = {
            "task_status": "active",  # Update session state
            # "user:login_count": session.state.get("user:login_count", 0) + 1, # Update user state
            # "user:last_login_ts": current_time,   # Add user state
            # "temp:validation_needed": True        # Add temporary state (will be discarded)
        }

        # --- Create Event with Actions ---
        actions_with_update = EventActions(state_delta=state_changes)
        # This event might represent an internal system action, not just an agent response
        system_event = Event(
            invocation_id="inv_login_update",
            author="system",  # Or 'agent', 'tool' etc.
            actions=actions_with_update,
            # timestamp=current_time
            # content might be None or represent the action taken
        )

        # --- Append the Event (This updates the state) ---
        # callback_context.session_service.append_event(session, system_event)
        # callback_context.state.update(
        #     {
        #         "browser_config444agent_init": {
        #             "browser_type": "chrome",
        #             "browser_path": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        #         }
        #     }
        # )
        return None


def before_tool_callback(
    tool: BaseTool, args: Dict[str, Any], tool_context: ToolContext
):
    """
    在 tool 执行前, 设置获取或者初始化浏览器配置
    """
    agent_name = tool_context.agent_name
    tool_name = tool.name
    # print(f"[Callback] Before tool call for tool '{tool_name}' in agent '{agent_name}'")
    # print(f"[Callback] Original args: {args}")

    if tool_name == "browser_use_tool" or tool_name == "browser_use_steal_tool":
        # 调用浏览器工具前, 先初始化 浏览器配置, 包括 浏览器指纹, 网络代理, 浏览器配置
        logger.warning(
            "TODO: 调用浏览器工具前, 先初始化 浏览器配置, 包括 浏览器指纹, 网络代理, 浏览器配置"
        )
        # 可以这样设置 state
        # tool_context.state.update({"browser_config222": {"browser_type": "chrome"}})
    return None


def after_tool_callback(
    tool: BaseTool,
    args: Dict[str, Any],
    tool_context: ToolContext,
    tool_response: Dict,
):
    """
    在 tool 执行后, 设置获取或者初始化浏览器配置
    """
    logger.warning(f"tool_response: {tool_response}")


def create_browser_agent():
    from mtmai.tools.browser_tool import browser_use_tool

    return Agent(
        model=get_default_litellm_model(),
        name="web_browser_agent",
        description="网页浏览器操作助理,可以根据任务描述,自动浏览网页,获取网页内容,和模拟用户的操作,使用自主多步骤的流程,完成任务",
        instruction=dedent(
            """你是专业操作浏览器的助手,擅长根据用户的对话上下文调用工具完成用户的指定任务.
**重要**:
    - 工具是开源 browser use, 版本号是 v0.1.40, 你必须一次性通过自然语音的描述将完整的任务交代清楚,
    - browser use 本身是 ai agent 可以理解你的任务并且内部能智能规划通过多个步骤操作浏览器来完成你给出的任务.
    - browser use 在任务结束后给你返回任务的最终结果描述, 并且会将任务的相关状态保存. 你可以在下一轮对话中获取到任务的结果的详细描述以及关键状态数据
    - 如果任务需要一些基本的资料, 应该在任务描述中附带. 特别是 账号, 网址, 等等.
    - 你需要完全明白浏览器所需的任务规划, 给出经过优化的步骤规划指引 browser use 操作
    - 你需要完全了解用户的意图以及任务涉及网站的相关特性
    - 如果需要人工操作, 请使用 browser_human_interaction_tool 工具.
      需要人工操作的常见场景: 人机检测, 验证码接收...
工具指引:
    browser_use_tool: 用于完成通用浏览器操作任务
    browser_use_steal_tool: 创建独立浏览器配置文件, 使用特定的 网络代理 和 浏览器指纹配置,防止账号间关联
"""
        ),
        tools=[
            browser_use_tool,
            # browser_use_steal_tool,
            # browser_human_interaction_tool,
        ],
        before_agent_callback=before_agent_callback,
        before_tool_callback=before_tool_callback,
    )


# 新代码开始 -----------------------------------------------------------------------------------------------
async def setup_playwright_context(browseruse_context: PlaywrightBrowserContext):
    await browseruse_context.add_init_script(
        """
        console.log("hello world===============@ browser_use_tool")
        """
    )

    # 额外的反检测脚本
    async def load_undetect_script():
        undetect_script = open(
            "packages/mtmai/mtmai/mtlibs/browser_utils/stealth_js/undetect_script.js",
            "r",
        ).read()
        return undetect_script

    await browseruse_context.add_init_script(await load_undetect_script())

    await browseruse_context.add_cookies(
        [
            {
                "name": "cookiesExampleEnabled2222detector",
                "value": "true",
                "url": "https://bot-detector.rebrowser.net",
            }
        ]
    )
    # 添加 cookies(演示)
    await browseruse_context.add_cookies(
        [
            {
                "name": "cookiesExampleEnabled2222detector",
                "value": "true",
                "url": "https://bot-detector.rebrowser.net",
            }
        ]
    )


class AdkBrowserAgent(BaseAgent):
    """
    使用 adk agent 封装 browser use 的 agent
    1: browser use 的步骤可以同步转换为 adk 的 event 事件
    """

    model_config = {"arbitrary_types_allowed": True}

    def __init__(
        self,
        name: str,
        description: str = "通过操作web browser 完成用户输入的任务",
    ):
        super().__init__(
            name=name,
            description=description,
        )

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """
        Implements the custom orchestration logic for the story workflow.
        Uses the instance attributes assigned by Pydantic (e.g., self.story_generator).
        """

        try:
            llm = ChatGoogleGenerativeAI(
                model="gemini-2.0-flash-exp",
                api_key=SecretStr(settings.GOOGLE_AI_STUDIO_API_KEY),
            )
            user_input_task = ctx.user_content.parts[0].text
            event_queue = []

            # Create an async event generator
            async def event_generator():
                while True:
                    if event_queue:
                        yield event_queue.pop(0)
                    else:
                        await asyncio.sleep(0.1)  # Small delay to prevent busy waiting

            # Start the event generator
            event_gen = event_generator()

            def browseruse_new_step_cb(state, step, step_index):
                event_queue.append(
                    Event(
                        author=self.name,
                        content=types.Content(
                            role="assistant",
                            parts=[types.Part(text=f"浏览器步骤{step_index}: {step}")],
                        ),
                    )
                )

            def browseruse_done_cb(history):
                event_queue.append(
                    Event(
                        author=self.name,
                        content=types.Content(
                            role="assistant",
                            parts=[types.Part(text=f"浏览器步骤完成: {history}")],
                        ),
                    )
                )

            helper = BrowseruseHelper()
            browser = await helper.get_browseruse_browser()

            browser_context = BrowseruseBrowserContext(
                browser=browser,
                config=BrowserContextConfig(
                    user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
                ),
            )

            async with browser_context as context:
                await setup_playwright_context(context.session.context)
                yield Event(
                    author="browser",
                    content=types.Content(
                        role="assistant",
                        parts=[types.Part(text="开始使用浏览器")],
                    ),
                )
                browser_user_agent = BrowseruseAgent(
                    task=user_input_task,
                    llm=llm,
                    use_vision=False,
                    browser_context=context,
                    max_actions_per_step=3,
                    register_new_step_callback=browseruse_new_step_cb,
                    register_done_callback=browseruse_done_cb,
                )

                # Start browser operations in the background
                browser_task = asyncio.create_task(browser_user_agent.run(max_steps=25))
                try:
                    # Yield events as they come in
                    while not browser_task.done():
                        async for event in event_gen:
                            yield event
                        await asyncio.sleep(0.1)  # Small delay to prevent busy waiting

                    # Get the final result
                    history: AgentHistoryList = await browser_task
                    final_result = history.final_result()
                    yield Event(
                        author=self.name,
                        content=types.Content(
                            role="assistant",
                            parts=[types.Part(text=final_result)],
                        ),
                    )
                except Exception as e:
                    logger.error(f"Error during browser operations: {str(e)}")
                    yield Event(
                        author=self.name,
                        content=types.Content(
                            role="assistant",
                            parts=[types.Part(text=f"浏览器操作出错: {str(e)}")],
                        ),
                    )
                    raise
        except Exception as e:
            logger.error(f"Error in _run_browseruse_agent: {str(e)}")
            yield Event(
                author=self.name,
                content=types.Content(
                    role="assistant",
                    parts=[types.Part(text=f"浏览器代理运行出错: {str(e)}")],
                ),
            )
            raise
