from loguru import logger
from smolagents import CodeAgent
from smolagents.agents import ActionStep

from mtmai.model_client import get_custom_model
from mtmai.tools.instagram_tool import InstagramLoginTool


def my_step_callback(memory_step: ActionStep, agent: CodeAgent) -> None:
    # sleep(1.0)  # Let JavaScript animations happen before taking the screenshot
    # driver = helium.get_driver()
    # current_step = memory_step.step_number
    # if driver is not None:
    #     for previous_memory_step in agent.memory.steps:  # Remove previous screenshots from logs for lean processing
    #         if isinstance(previous_memory_step, ActionStep) and previous_memory_step.step_number <= current_step - 2:
    #             previous_memory_step.observations_images = None
    #     png_bytes = driver.get_screenshot_as_png()
    #     image = PIL.Image.open(BytesIO(png_bytes))
    #     print(f"Captured a browser screenshot: {image.size} pixels")
    #     memory_step.observations_images = [image.copy()]  # Create a copy to ensure it persists, important!

    # # Update observations with current URL
    # url_info = f"Current url: {driver.current_url}"
    # memory_step.observations = (
    #     url_info if memory_step.observations is None else memory_step.observations + "\n" + url_info
    # )
    logger.info(f"my_step_callback: {memory_step}")


def run_smola_agent():
    from smolagents import CodeAgent

    model = get_custom_model()
    # agent = CodeAgent(tools=[DuckDuckGoSearchTool()], model=model)
    agent = CodeAgent(
        tools=[InstagramLoginTool()],
        model=model,
        step_callbacks=[my_step_callback],
        max_steps=20,
        verbosity_level=2,
    )
    result = agent.run("使用工具, 登录到instagram, 然后获取我的粉丝列表")
    logger.info(f"result: {result}")
    yield result
