import os
from typing import AsyncGenerator, override

from google.adk.agents import LlmAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.genai import types  # noqa
from mtmai.model_client.utils import get_default_litellm_model


class ShortvideoAnalyticsAgent(LlmAgent()):
    model_config = {"arbitrary_types_allowed": True}

    def __init__(
        self,
        name: str,
        description: str = "给定视频, 分析视频的情感, 风格, 主题, 以及视频的受众群体",
        model: str = get_default_litellm_model(),
        **kwargs,
    ):
        super().__init__(
            name=name,
            description=description,
            model=model,
            **kwargs,
        )

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        user_content = ctx.user_content
        user_input_text = user_content.parts[0].text

        # 默认值
        ctx.session.state["video_subject"] = user_input_text
        ctx.session.state["paragraph_number"] = 3
        ctx.session.state["video_terms_amount"] = 3
        ctx.session.state["output_dir"] = f".vol/short_videos/{ctx.session.id}"
        async for event in self.sequential_agent.run_async(ctx):
            yield event
        os.makedirs(ctx.session.state["output_dir"], exist_ok=True)


def new_shortvideo_analytics_agent():
    return ShortvideoAnalyticsAgent(
        model=get_default_litellm_model(),
        name="shortvideo_analytics_agent",
    )
