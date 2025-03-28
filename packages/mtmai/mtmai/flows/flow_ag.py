from flows.flow_ctx import FlowCtx
from loguru import logger
from model_client.utils import get_custom_model
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.agent_run_input import AgentRunInput
from mtmai.clients.rest.models.flow_names import FlowNames
from mtmai.context.context import Context
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx, get_tenant_id
from mtmai.worker_app import mtmapp
from smolagents import CodeAgent
from smolagents.agents import ActionStep
from tools.instagram_tool import InstagramLoginTool


@mtmapp.workflow(
    name=FlowNames.AG,
    on_events=[f"{FlowNames.AG}"],
)
class FlowAg:
    @mtmapp.step(timeout="60m")
    async def entry(self, hatctx: Context):
        """
        设计概要:
        1: 入口可以理解为一个团队,Agent,或一个langgraph的flow
        2: 入口 使用 session_id 来标识团队的状态
        3: autogen 的内置团队看起来没有达到预期的设计目标, 因此不要过度依赖 autogen 的组件.
        4: 类似 autogen 中的 team 状态管理,多智能体间对话的实现, 完全可以使用 hatchet 工作流来实现.
        """
        flowctx = FlowCtx().from_hatctx(hatctx)
        input = AgentRunInput.model_validate(hatctx.input)
        cancellation_token = MtCancelToken()
        tenant_client = TenantClient()
        session_id = get_chat_session_id_ctx()
        tid = get_tenant_id()
        if not tid:
            raise ValueError("tenant_id is required")

        # 1: 加载 agent
        #    原因: 所谓的智能体编排实际是由一个 supervisor agent 通过 消息类型决定调用下一个子流程
        #    hatchet 的子工作流,本身支持并发.

        # agent = await flowctx.load_agent(input.component_id)
        # if session_id:
        #     # TODO: 加载agent state
        #     pass

        # task = """调用工具,获取这个页面: https://docs.postiz.com/providers/instagram, 然后总结这个页面的内容提要"""
        # output_stream = agent.on_messages_stream(
        #     [TextMessage(content=task, source="user")],
        #     cancellation_token=CancellationToken(),
        # )
        # last_txt_message = ""
        # async for message in output_stream:
        #     if isinstance(message, ToolCallRequestEvent):
        #         for tool_call in message.content:
        #             logger.info(f"  [acting]! Calling {tool_call.name}... [/acting]")

        #     if isinstance(message, ToolCallExecutionEvent):
        #         for result in message.content:
        #             # Compute formatted text separately to avoid backslashes in the f-string expression.
        #             formatted_text = result.content[:200].replace("\n", r"\n")
        #             logger.info(f"  [observe]> {formatted_text} [/observe]")

        #     if isinstance(message, Response):
        #         if isinstance(message.chat_message, TextMessage):
        #             last_txt_message += message.chat_message.content
        #         elif isinstance(message.chat_message, ToolCallSummaryMessage):
        #             content = message.chat_message.content
        #             # only print the first 100 characters
        #             # console.print(Panel(content[:100] + "...", title="Tool(s) Result (showing only 100 chars)"))
        #             last_txt_message += content
        #         else:
        #             raise ValueError(f"Unexpected message type: {message.chat_message}")
        #         logger.info(last_txt_message)

        for result in run_smola_agent():
            logger.info(f"result: {result}")

        logger.info(f"(FlowAg)工作流结束,{hatctx.step_run_id}\n")
        return {"result": "todo"}


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
    # return
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
