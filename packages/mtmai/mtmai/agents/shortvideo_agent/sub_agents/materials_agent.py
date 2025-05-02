import json
from typing import AsyncGenerator, override

from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.genai import types
from mtmai.mpt.services import material  # noqa


class MaterialsAgent(BaseAgent):
    """
    根据文案和字幕,通过 api 获取素材
    """

    model_config = {"arbitrary_types_allowed": True}

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        output_dir = ctx.session.state["output_dir"]

        video_terms = ctx.session.state["video_terms"]
        if isinstance(video_terms, str):
            video_terms = json.loads(video_terms.strip())

        downloaded_videos = material.download_videos(
            output_dir=output_dir,
            search_terms=video_terms,
        )
        if not downloaded_videos:
            yield Event(
                author=ctx.agent.name,
                content=types.Content(
                    role="assistant",
                    parts=[types.Part(text="素材收集失败")],
                ),
            )
            return
        yield Event(
            author=ctx.agent.name,
            content=types.Content(
                role="assistant",
                parts=[
                    types.Part(
                        text="素材收集完成, 素材数量: {}".format(len(downloaded_videos))
                    )
                ],
            ),
            actions={
                "state_delta": {
                    "downloaded_videos": downloaded_videos,
                },
            },
        )
