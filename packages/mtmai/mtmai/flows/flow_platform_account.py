from clients.rest.models.flow_names import FlowNames
from flows.flow_ctx import FlowCtx
from loguru import logger
from mtmai.agents.cancel_token import MtCancelToken
from mtmai.clients.rest.models.platform_account_flow_input import (
    PlatformAccountFlowInput,
)
from mtmai.context.context import Context
from mtmai.context.context_client import TenantClient
from mtmai.context.ctx import get_chat_session_id_ctx, get_tenant_id
from mtmai.worker_app import mtmapp


@mtmapp.workflow(
    name=FlowNames.PLATFORM_ACCOUNT,
    on_events=[f"{FlowNames.PLATFORM_ACCOUNT}"],
)
class FlowPlatformAccount:
    @mtmapp.step(timeout="5m")
    async def entry(self, hatctx: Context):
        """
        社交媒体账号的初始化
        """
        flowctx = FlowCtx().from_hatctx(hatctx)
        input = PlatformAccountFlowInput.model_validate(hatctx.input)
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

        # for result in run_smola_agent():
        #     logger.info(f"result: {result}")

        logger.info(f"(FlowPlatformAccount)工作流结束,{hatctx.step_run_id}\n")
        return {"result": "todo"}
