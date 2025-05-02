from google.adk.agents import LlmAgent
from google.genai import types  # noqa
from mtmai.model_client.utils import get_default_litellm_model

# class VideoScriptAgent(BaseAgent):
#     """
#     短视频文案生成专家
#     """

#     model_config = {"arbitrary_types_allowed": True}

#     def __init__(
#         self, name: str, description: str, model: str = get_default_litellm_model()
#     ):
#         super().__init__(
#             name,
#             description,
#             model,
#         )

#     @override
#     async def _run_async_impl(
#         self, ctx: InvocationContext
#     ) -> AsyncGenerator[Event, None]:
#         output_dir = ctx.session.state["output_dir"]

#         yield Event(
#             author=ctx.agent.name,
#             content=types.Content(
#                 role="assistant",
#                 parts=[types.Part(text="文案生成成功")],
#             ),
#             actions={
#                 "state_delta": {
#                     # "audio_file": audio_file,
#                     # "audio_duration": audio_duration,
#                     # "subtitle_path": subtitle_path,
#                 },
#             },
#         )


def new_videoscript_agent():
    video_script_agent = LlmAgent(
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
    return video_script_agent
