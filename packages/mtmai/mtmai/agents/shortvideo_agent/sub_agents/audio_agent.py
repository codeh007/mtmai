import math
import os.path
from os import path
from typing import AsyncGenerator, override

from google.adk.agents import LlmAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.genai import types  # noqa
from mtmai.core.config import settings
from mtmai.model_client.utils import get_default_litellm_model
from mtmai.NarratoAI.services import subtitle, voice

SPEECH_PROMPT = """
你是一个有10年经验的短视频生成专家, 擅长短视频相关的完整的操作流程,包括文案创作, 视频拍摄, 视频剪辑, 视频特效, 视频配音, 视频字幕, 视频封面, 视频发布等.

**要求**
- 最终的视频,是适合发布到 tiktok 的短视频, 视频长度在 15 秒到 30 秒之间, 目的是吸引用户关注
- 整个操作过程, 不要打搅用户,应该尽你最大的能力, 帮助用户生成一个优质的短视频


"""


class AudioGenAgent(LlmAgent):
    """
    生成字幕和解说音频
    """

    model_config = {"arbitrary_types_allowed": True}

    def __init__(
        self,
        name: str,
        description: str,
        model: str = get_default_litellm_model(),
        **kwargs,
    ):
        super().__init__(
            name=name,
            description=description,
            model=model,
            # instruction=AUDIO_PROMPT,
            **kwargs,
        )

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        output_dir = ctx.session.state["output_dir"]
        # 生成 音频讲解
        video_script = ctx.session.state["video_script"]
        voice_name = ctx.session.state["voice_name"]
        output_audio_file = path.join(output_dir, "audio.mp3")
        sub_maker = await voice.tts_edgetts(
            text=video_script,
            voice_name=voice.parse_voice_name(voice_name),
            # voice_rate=voice_rate,
            voice_file=output_audio_file,
        )
        if sub_maker is None:
            raise ValueError("failed to generate audio, sub_maker is None")

        audio_duration = math.ceil(voice.get_audio_duration(sub_maker))

        if not output_audio_file:
            yield Event(
                author=ctx.agent.name,
                content=types.Content(
                    role="assistant",
                    parts=[types.Part(text="音频生成失败")],
                ),
            )
            return

        # 上传
        audio_file_bytes = open(output_audio_file, "rb").read()
        mp3_part = types.Part(
            inline_data=types.Blob(data=audio_file_bytes, mime_type="audio/mpeg")
        )

        await ctx.artifact_service.save_artifact(
            app_name=ctx.agent.name,
            user_id=settings.DEMO_USER_ID,  # TODO: 修正 user_id
            session_id=ctx.session.id,
            filename="speech.mp3",
            artifact=mp3_part,
        )
        yield Event(
            author=ctx.agent.name,
            content=types.Content(
                role="assistant",
                parts=[
                    types.Part(
                        text="音频生成成功",
                        file_data=types.FileData(
                            file_uri=f"user:{ctx.session.id}/speech.mp3",
                            mime_type="audio/mpeg",
                        ),
                    )
                ],
            ),
            actions={
                "state_delta": {
                    "audio_file": output_audio_file,
                    "audio_duration": audio_duration,
                },
                "artifact_delta": {
                    "audio.mp3": 1,
                },
            },
        )

        # 生成字幕

        subtitle_fallback = False
        subtitle_path = path.join(output_dir, "subtitle.srt")
        subtitle_provider = ctx.session.state["voice_llm_provider"]
        if subtitle_provider == "edgetts":
            voice.create_subtitle(
                text=video_script, sub_maker=sub_maker, subtitle_file=subtitle_path
            )
            if not os.path.exists(subtitle_path):
                subtitle_fallback = True
                raise ValueError(
                    f"failed to generate subtitle, subtitle_path: {subtitle_path}"
                )

        elif subtitle_provider == "whisper" or subtitle_fallback:
            subtitle.create(audio_file=output_audio_file, subtitle_file=subtitle_path)
            subtitle.correct(subtitle_file=subtitle_path, video_script=video_script)

        else:
            raise ValueError(f"unknown subtitle provider: {subtitle_provider}")

        subtitle_srt = subtitle.file_to_subtitles(subtitle_path)

        if not subtitle_srt:
            raise ValueError("failed to generate subtitle_srt")

        subtitle_file_bytes = open(subtitle_path, "rb").read()
        srt_part = types.Part(
            inline_data=types.Blob(data=subtitle_file_bytes, mime_type="text/plain")
        )
        await ctx.artifact_service.save_artifact(
            app_name=ctx.agent.name,
            user_id=settings.DEMO_USER_ID,  # TODO: 修正 user_id
            session_id=ctx.session.id,
            filename="subtitle.srt",
            artifact=srt_part,
        )
        yield Event(
            author=ctx.agent.name,
            content=types.Content(
                role="assistant",
                parts=[
                    types.Part(
                        text="字幕生成成功",
                        file_data=types.FileData(
                            file_uri=f"user:{ctx.session.id}/subtitle.srt",
                            mime_type="text/plain",
                        ),
                    ),
                ],
            ),
            actions={
                "state_delta": {
                    "subtitle": subtitle_srt,
                    "subtitle_path": subtitle_path,
                },
                "artifact_delta": {
                    "subtitle.srt": 1,
                },
            },
        )
