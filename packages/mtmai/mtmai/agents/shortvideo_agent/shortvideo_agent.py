import os
from typing import AsyncGenerator, override

from google.adk.agents import BaseAgent, SequentialAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.genai import types  # noqa
from mtmai.agents.shortvideo_agent.sub_agents.process_agent import (
    new_video_process_agent,
)
from mtmai.model_client.utils import get_default_litellm_model


class ShortvideoAgent(BaseAgent):
    model_config = {"arbitrary_types_allowed": True}

    sequential_agent: SequentialAgent

    def __init__(
        self,
        name: str,
        description: str = "短视频生成专家",
        model: str = get_default_litellm_model(),
        **kwargs,
    ):
        super().__init__(
            name=name,
            description=description,
            sequential_agent=new_video_process_agent(),
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


def new_shortvideo_agent():
    return ShortvideoAgent(
        model=get_default_litellm_model(),
        name="shortvideo_generator_agent",
    )
