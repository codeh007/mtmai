from autogen_core import MessageContext, RoutedAgent, message_handler

from mtmai.agents._types import BrowserOpenTask


class BrowserAgent(RoutedAgent):
    def __init__(
        self, description: str, agent_topic_type: str, user_topic_type: str
    ) -> None:
        super().__init__(description)

    @message_handler
    async def handle_user_task(
        self, message: BrowserOpenTask, ctx: MessageContext
    ) -> None:
        from browser_use import Agent, Browser

        agent = Agent()
        browser = Browser()
        page = browser.new_page()
        page.goto("https://playwright.dev/")
