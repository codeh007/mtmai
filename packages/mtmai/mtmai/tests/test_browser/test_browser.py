import pytest

# from loguru import logger
from mtmai.hatchet import Hatchet
from mtmai.mtlibs.browser_utils.browser_manager import MtBrowserManager
from mtmai.worker.worker import Worker


@pytest.mark.asyncio
async def test_browser1(mtmapp: Hatchet, worker: Worker) -> None:
    async with MtBrowserManager(
        config={},
    ) as browser_manager:
        async with await browser_manager.get_browseruse_context() as browseruse_context:
            # 从 state 加载 cookies
            # browser_cookies = tool_context.state.get(STATE_KEY_BROWSER_COOKIES, None)
            # if browser_cookies:
            #     browseruse_context.session.context.add_cookies(browser_cookies)

            # await setup_context(browseruse_context.session.context)

            # steal_agent = BrowserUserAgent(
            #     # 其他 人机检测网站: https://bot.sannysoft.com/
            #     task="""
            #         访问: https://bot-detector.rebrowser.net/ , 根据页面内容告我我是否已经通过了人机检测, 如果没有通过,具体原因是什么?
            #     """,
            #     llm=llm,
            #     browser_context=browseruse_context,
            # )
            # steal_history = await steal_agent.run(max_steps=5)

            # 保存相关 状态到 state
            cookies = await browseruse_context.session.context.cookies()
