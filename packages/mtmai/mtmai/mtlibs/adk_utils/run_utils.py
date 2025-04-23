import asyncio

from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.genai import types
from loguru import logger
from smolagents import ActionStep, CodeAgent


async def adk_run_smolagent(agent: CodeAgent, ctx: InvocationContext):
    """
    在 adk agent 上下文中运行 smolagents 的 CodeAgent, 并且并对相关事件进行转换

    例子:
    ```python
        agent = CodeAgent(
            tools=[],
            model=get_default_smolagents_model(),
            additional_authorized_imports=["helium", "re", "httpx"],
            max_steps=20,
            verbosity_level=2,
            # step_callbacks=[step_callback],
        )
        async for event in adk_run_smolagent(agent=agent, ctx=ctx):
            yield event
    ```
    """

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
                    author=ctx.agent.name,
                    content=types.Content(
                        role=message["role"],
                        parts=[
                            types.Part(text=f"执行步骤: {step.step_number}: {text}")
                        ],
                    ),
                )
            )

    agent.step_callbacks = [*agent.step_callbacks, step_callback]
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
            author=ctx.agent.name,
            content=types.Content(
                role="assistant",
                parts=[types.Part(text=f"执行完成: {result}")],
            ),
        )
    except Exception as e:
        logger.error(f"Error during agent execution: {str(e)}")
        yield Event(
            author=ctx.agent.name,
            content=types.Content(
                role="assistant",
                parts=[types.Part(text=f"执行出错: {str(e)}")],
            ),
        )
        raise
