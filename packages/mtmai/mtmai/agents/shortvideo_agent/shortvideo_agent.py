import os
from typing import AsyncGenerator, override

from google.adk.agents import BaseAgent, LlmAgent, SequentialAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.genai import types  # noqa
from mtmai.agents.shortvideo_agent.sub_agents.audio_agent import AudioGenAgent
from mtmai.agents.shortvideo_agent.sub_agents.materials_agent import MaterialsAgent
from mtmai.model_client.utils import get_default_litellm_model
from mtmai.mpt.models.schema import VideoAspect, VideoParams, VideoTransitionMode

from .sub_agents.finnal_gen_video import FinalGenVideoAgent


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
        video_script_generator = LlmAgent(
            name="VideoScriptGenerator",
            model=get_default_litellm_model(),
            instruction="""
# Role: Video Script Generator

## Goals:
Generate a script for a video, depending on the subject of the video.

## Constrains:
1. the script is to be returned as a string with the specified number of paragraphs.
2. do not under any circumstance reference this prompt in your response.
3. get straight to the point, don't start with unnecessary things like, "welcome to this video".
4. you must not include any type of markdown or formatting in the script, never use a title.
5. only return the raw content of the script.
6. do not include "voiceover", "narrator" or similar indicators of what should be spoken at the beginning of each paragraph or line.
7. you must not mention the prompt, or anything about the script itself. also, never talk about the amount of paragraphs or lines. just write the script.
8. respond in the same language as the video subject.

# Initialization:
- number of paragraphs: {paragraph_number}
""".strip(),
            input_schema=None,
            output_key="video_script",  # Key for storing output in session state
        )

        video_terms_generator = LlmAgent(
            name="VideoTermsGenerator",
            model=get_default_litellm_model(),
            instruction="""
# Role: Video Search Terms Generator

## Goals:
Generate {video_terms_amount} search terms for stock videos, depending on the subject of a video.

## Constrains:
1. the search terms are to be returned as a json-array of strings.
2. each search term should consist of 1-3 words, always add the main subject of the video.
3. you must only return the json-array of strings. you must not return anything else. you must not return the script.
4. the search terms must be related to the subject of the video.
5. reply with english search terms only.

## Output Example:
["search term 1", "search term 2", "search term 3","search term 4","search term 5"]

## Context:
### Video Subject
{video_subject}

### Video Script
{video_script}

Please note that you must use English for generating video search terms; Chinese is not accepted.
""".strip(),
            input_schema=None,
            output_key="video_terms",  # Key for storing output in session state
        )

        video_subject_generator = LlmAgent(
            name="VideoSubjectGenerator",
            model=get_default_litellm_model(),
            instruction="""
# Role: Video Subject Generator

## Goals:
Generate a subject for a video, depending on the user's input.

## Constrains:
1. the subject is to be returned as a string.
2. the subject must be related to the user's input.
""".strip(),
            input_schema=None,
            output_key="video_subject",  # Key for storing output in session state
        )

        super().__init__(
            name=name,
            description=description,
            sequential_agent=SequentialAgent(
                name="ShortvideoProcessing",
                sub_agents=[
                    video_subject_generator,
                    video_script_generator,
                    video_terms_generator,
                    AudioGenAgent(
                        name="AudioGenAgent",
                        description="生成音频",
                    ),
                    MaterialsAgent(
                        name="MaterialsAgent",
                        description="根据文案和字幕,通过 api 获取素材",
                    ),
                    FinalGenVideoAgent(
                        name="FinalGenVideoAgent",
                        description="根据最终的视频生成参数, 合并生成最终的视频",
                    ),
                ],
            ),
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
        ctx.session.state["output_dir"] = f".vol/short_videos/{ctx.invocation_id}"

        async for event in self.sequential_agent.run_async(ctx):
            yield event
        os.makedirs(ctx.session.state["output_dir"], exist_ok=True)

        ctx.session.state["video_params"] = VideoParams(
            video_subject=ctx.session.state.get("video_subject"),
            video_script=ctx.session.state.get("video_script"),
            video_terms=ctx.session.state.get("video_terms"),
            video_aspect=VideoAspect.portrait,
            voice_name="zh-CN-XiaoxiaoNeural",
            voice_rate="1.0",
            bgm_type="random",
            bgm_file="./mtmai/resources/songs/output001.mp3",
            text_color="#FFFFFF",
            font_size=60,
            stroke_color="#000000",
            video_transition_mode=VideoTransitionMode.fade_in,
            subtitle_enabled=True,
        ).model_dump()

        yield Event(
            author=ctx.agent.name,
            content=types.Content(
                role="assistant",
                parts=[
                    types.Part(
                        text="结束",
                    ),
                ],
            ),
        )


def new_shortvideo_agent():
    return ShortvideoAgent(
        model=get_default_litellm_model(),
        name="shortvideo_generator_agent",
    )
