import os
from typing import AsyncGenerator, override

from google.adk.agents import LlmAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.adk.tools.agent_tool import AgentTool
from google.genai import types  # noqa
from mtmai.agents.shortvideo_agent.shortvideo_prompts import SHORTVIDEO_PROMPT

# from mtmai.agents.shortvideo_agent.tools.gen_speech_tool import gen_speech_tool
from mtmai.agents.shortvideo_agent.sub_agents.audio_agent import AudioGenAgent
from mtmai.model_client.utils import get_default_litellm_model

video_subject_generator = LlmAgent(
    name="video_subject_generator",
    description="视频主题生成专家",
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

video_script_agent = LlmAgent(
    name="VideoScriptGenerator",
    model=get_default_litellm_model(),
    description="视频脚本生成专家",
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
    output_key="video_script",
)


class ShortvideoAgent(LlmAgent):
    model_config = {"arbitrary_types_allowed": True}

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
            model=model,
            instruction=SHORTVIDEO_PROMPT,
            tools=[
                AgentTool(video_subject_generator),
                AgentTool(video_script_agent),
                AgentTool(
                    AudioGenAgent(
                        name="audio_gen_agent",
                        description="音频生成专家",
                        model=model,
                        tools=[],
                        input_schema=None,
                        output_key="audio_file",
                    )
                ),
            ],
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
        ctx.session.state["voice_name"] = "zh-CN-XiaoxiaoNeural"
        ctx.session.state["voice_llm_provider"] = "edgetts"
        os.makedirs(ctx.session.state["output_dir"], exist_ok=True)

        async for event in super()._run_async_impl(ctx):
            yield event


def new_shortvideo_agent():
    return ShortvideoAgent(
        model=get_default_litellm_model(),
        name="shortvideo_generator",
        description="短视频生成专家",
    )
