from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_core.models import ChatCompletionClient
from loguru import logger

from mtmai.agents._types import BrowserOpenTask, BrowserTask


class BrowserAgent(RoutedAgent):
    def __init__(self, description: str, model_client: ChatCompletionClient) -> None:
        super().__init__(description)
        self.model_client = model_client

    @message_handler
    async def handle_browser_open_task(
        self, message: BrowserOpenTask, ctx: MessageContext
    ) -> None:
        from browser_use import Agent, Browser

        agent1 = Agent()
        await agent1.run()

        browser = Browser()
        page = browser.new_page()
        page.goto("https://playwright.dev/")

    @message_handler
    async def handle_browser_task(
        self, message: BrowserTask, ctx: MessageContext
    ) -> None:
        logger.info("(BrowserTask)")
        pass
