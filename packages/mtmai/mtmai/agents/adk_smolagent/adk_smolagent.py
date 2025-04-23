import asyncio
from typing import AsyncGenerator

from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.adk.tools import ToolContext
from google.genai import types  # noqa: F401
from loguru import logger
from smolagents import ActionStep, CodeAgent
from typing_extensions import override

from mtmai.model_client.utils import get_default_smolagents_model


class AdkSmolAgent(BaseAgent):
    """
    用 adk agent 封装 smolagent 的 CodeAgent

    """

    model_config = {"arbitrary_types_allowed": True}

    def __init__(
        self,
        name: str,
        description: str = "擅长使用 python 解决复杂任务",
    ):
        super().__init__(
            name=name,
            description=description,
        )

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        logger.info(f"[{self.name}] Starting story generation workflow.")
        user_input_task = ctx.user_content.parts[0].text
        event_queue = []

        # Create an async event generator
        async def event_generator():
            while True:
                if event_queue:
                    yield event_queue.pop(0)
                else:
                    await asyncio.sleep(0.1)  # Small delay to prevent busy waiting

        event_gen = event_generator()

        def step_callback(step: ActionStep) -> None:
            # TODO: 消息格式转换需要更加深入
            smolagent_messages = step.to_messages()
            for message in smolagent_messages:
                text = message["content"][0]["text"]
                event_queue.append(
                    Event(
                        author=self.name,
                        content=types.Content(
                            role=message["role"],
                            parts=[
                                types.Part(text=f"执行步骤: {step.step_number}: {text}")
                            ],
                        ),
                    )
                )

        agent = CodeAgent(
            tools=[],
            model=get_default_smolagents_model(),
            additional_authorized_imports=["helium", "re", "httpx"],
            max_steps=20,
            verbosity_level=2,
            step_callbacks=[step_callback],
        )

        # Start agent operations in the background
        agent_task = asyncio.get_event_loop().run_in_executor(
            None,
            agent.run,
            user_input_task,
        )

        try:
            while not agent_task.done():
                async for event in event_gen:
                    yield event
                await asyncio.sleep(0.1)

            # Get the final result
            result = await agent_task
            yield Event(
                author=self.name,
                content=types.Content(
                    role="assistant",
                    parts=[types.Part(text=f"执行完成: {result}")],
                ),
            )
        except Exception as e:
            logger.error(f"Error during agent execution: {str(e)}")
            yield Event(
                author=self.name,
                content=types.Content(
                    role="assistant",
                    parts=[types.Part(text=f"执行出错: {str(e)}")],
                ),
            )
            raise


# @deprecated 应优先 以 agent 的方式实现.
async def adk_smolagent_browser_automation_tool(
    task: str, tool_context: ToolContext
) -> dict[str, str]:
    """基于 smolagent 的浏览器自动化操作

    Args:
        task: 需要执行的任务
        tool_context: ToolContext object.
    Returns:
        操作的最终结果
    """
    # Configure Chrome options
    # chrome_options = webdriver.ChromeOptions()
    # # chrome_options.add_argument("--force-device-scale-factor=1")
    # # chrome_options.add_argument("--window-size=1000,1350")
    # # chrome_options.add_argument("--disable-pdf-viewer")
    # chrome_options.add_argument("--window-position=0,0")

    # # Initialize the browser
    # driver = helium.start_chrome(
    #     headless=False, url="https://www.bing.com", options=chrome_options
    # )

    # @tool
    # def search_item_ctrl_f(text: str, nth_result: int = 1) -> str:
    #     """
    #     Searches for text on the current page via Ctrl + F and jumps to the nth occurrence.
    #     Args:
    #         text: The text to search for
    #         nth_result: Which occurrence to jump to (default: 1)
    #     """
    #     elements = driver.find_elements(By.XPATH, f"//*[contains(text(), '{text}')]")
    #     if nth_result > len(elements):
    #         raise Exception(
    #             f"Match n°{nth_result} not found (only {len(elements)} matches found)"
    #         )
    #     result = f"Found {len(elements)} matches for '{text}'."
    #     elem = elements[nth_result - 1]
    #     driver.execute_script("arguments[0].scrollIntoView(true);", elem)
    #     result += f"Focused on element {nth_result} of {len(elements)}"
    #     return result

    # @tool
    # def go_back() -> None:
    #     """Goes back to previous page."""
    #     driver.back()

    # @tool
    # def close_popups() -> str:
    #     """
    #     Closes any visible modal or pop-up on the page. Use this to dismiss pop-up windows!
    #     This does not work on cookie consent banners.
    #     """
    #     driver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

    # Set up screenshot callback
    # def save_screenshot(memory_step: ActionStep, agent: CodeAgent) -> None:
    #     sleep(1.0)  # Let JavaScript animations happen before taking the screenshot
    #     driver = helium.get_driver()
    #     current_step = memory_step.step_number
    #     if driver is not None:
    #         for (
    #             previous_memory_step
    #         ) in agent.memory.steps:  # Remove previous screenshots for lean processing
    #             if (
    #                 isinstance(previous_memory_step, ActionStep)
    #                 and previous_memory_step.step_number <= current_step - 2
    #             ):
    #                 previous_memory_step.observations_images = None
    #         png_bytes = driver.get_screenshot_as_png()
    #         image = Image.open(BytesIO(png_bytes))
    #         print(f"Captured a browser screenshot: {image.size} pixels")
    #         memory_step.observations_images = [
    #             image.copy()
    #         ]  # Create a copy to ensure it persists

    #     # Update observations with current URL
    #     url_info = f"Current url: {driver.current_url}"
    #     memory_step.observations = (
    #         url_info
    #         if memory_step.observations is None
    #         else memory_step.observations + "\n" + url_info
    #     )

    # Initialize the model
    # model_id = "meta-llama/Llama-3.3-70B-Instruct"  # You can change this to your preferred model
    # model = HfApiModel(model_id=model3d)

    # Create the agent
    agent = CodeAgent(
        # tools=[go_back, close_popups, search_item_ctrl_f],
        tools=[],
        model=get_default_smolagents_model(),
        # additional_authorized_imports=["helium"],
        # step_callbacks=[take_screenshot],
        max_steps=20,
        verbosity_level=2,
    )

    # Import helium for the agent
    # agent.python_executor("from helium import *", agent.state)

    helium_instructions = """

    """
    agent_output = agent.run(task + helium_instructions)

    return agent_output
