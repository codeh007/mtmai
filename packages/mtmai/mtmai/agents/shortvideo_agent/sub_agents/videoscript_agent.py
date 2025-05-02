from typing import AsyncGenerator, override

from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.genai import types  # noqa
from mtmai.model_client.utils import get_default_litellm_model


class VideoScriptAgent(BaseAgent):
    """
    短视频文案生成专家
    """

    model_config = {"arbitrary_types_allowed": True}

    def __init__(
        self, name: str, description: str, model: str = get_default_litellm_model()
    ):
        super().__init__(
            name,
            description,
            model,
        )

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        output_dir = ctx.session.state["output_dir"]

        yield Event(
            author=ctx.agent.name,
            content=types.Content(
                role="assistant",
                parts=[types.Part(text="文案生成成功")],
            ),
            actions={
                "state_delta": {
                    # "audio_file": audio_file,
                    # "audio_duration": audio_duration,
                    # "subtitle_path": subtitle_path,
                },
            },
        )
