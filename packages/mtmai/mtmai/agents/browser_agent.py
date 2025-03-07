import logging

from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_ext.models.openai import OpenAIClientConfigurationConfigModel
from loguru import logger

from mtmai.agents._types import BrowserOpenTask, BrowserTask
from mtmai.agents.model_client import MtmOpenAIChatCompletionClient

logger2 = logging.getLogger("browser_use")
logger2.setLevel(logging.DEBUG)


class BrowserAgent(RoutedAgent):
    def __init__(
        self, description: str, model_client: MtmOpenAIChatCompletionClient
    ) -> None:
        super().__init__(description)
        self.model_client = model_client

    @message_handler
    async def handle_browser_open_task(
        self, message: BrowserOpenTask, ctx: MessageContext
    ) -> None:
        from browser_use import Agent, Browser

        ag_model_config: OpenAIClientConfigurationConfigModel = (
            self.model_client._to_config()
        )
        lc_model = self.model_client.convert_to_lc_model()
        browser = Browser()
        async with await browser.new_context() as context:
            agent1 = Agent(
                task="Open an online code editor programiz.",
                llm=lc_model,
                browser_context=context,
                use_vision=False,
                use_vision_for_planner=False,
            )
            await agent1.run()

        # browser = Browser()
        page = browser.new_page()
        page.goto("https://playwright.dev/")

    @message_handler
    async def handle_browser_task(
        self, message: BrowserTask, ctx: MessageContext
    ) -> None:
        logger.info("(BrowserTask)")
        pass
