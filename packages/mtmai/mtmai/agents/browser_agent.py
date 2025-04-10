import logging

from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_core.models import ChatCompletionClient
from loguru import logger
from mtlibs.autogen_utils._types import BrowserOpenTask, BrowserTask

logger2 = logging.getLogger("browser_use")
logger2.setLevel(logging.DEBUG)


class BrowserAgent(RoutedAgent):
    def __init__(self, description: str, model_client: ChatCompletionClient) -> None:
        super().__init__(description)
        self.model_client = model_client

    @message_handler
    async def handle_browser_open_task(
        self, message: BrowserOpenTask, ctx: MessageContext
    ) -> None:
        from mtmai.browser_use import Browser

        browser = Browser()
        browser_context = await browser.new_context()
        # async with await browser.new_context() as context:
        page = await browser_context.get_current_page()
        await page.goto("https://playwright.dev/")

        ...

        # browser = Browser()
        # page = browser.new_page()
        # page.goto("https://playwright.dev/")

    @message_handler
    async def handle_browser_task(
        self, message: BrowserTask, ctx: MessageContext
    ) -> None:
        from mtmai.browser_use import Agent, Browser

        logger.info("(BrowserTask)")
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
