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
    event_queue = asyncio.Queue()

    def step_callback(step: ActionStep) -> None:
        # TODO: 消息格式转换需要更加深入
        smolagent_messages = step.to_messages()
        for message in smolagent_messages:
            text = message["content"][0]["text"]
            event = Event(
                author=ctx.agent.name,
                content=types.Content(
                    role=message["role"],
                    parts=[types.Part(text=f"执行步骤: {step.step_number}: {text}")],
                ),
            )
            # 直接将事件放入队列,不创建新的事件循环
            event_queue.put_nowait(event)

    agent.step_callbacks = [*agent.step_callbacks, step_callback]

    try:
        # Start agent operations in the background
        loop = asyncio.get_event_loop()
        agent_future = loop.run_in_executor(
            None,
            agent.run,
            user_input_task,
        )

        # Keep yielding events from queue until agent is done
        while not agent_future.done() or not event_queue.empty():
            try:
                event = await asyncio.wait_for(event_queue.get(), timeout=0.1)
                yield event
            except asyncio.TimeoutError:
                continue

        # Get the final result
        result = await agent_future
        completion_event = Event(
            author=ctx.agent.name,
            content=types.Content(
                role="assistant",
                parts=[types.Part(text=f"执行完成: {result}")],
            ),
        )
        yield completion_event

    except Exception as e:
        logger.error(f"Error during agent execution: {str(e)}")
        error_event = Event(
            author=ctx.agent.name,
            content=types.Content(
                role="assistant",
                parts=[types.Part(text=f"执行出错: {str(e)}")],
            ),
        )
        yield error_event
        raise
