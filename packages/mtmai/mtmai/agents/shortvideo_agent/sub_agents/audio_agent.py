import math
import os.path
from os import path
from typing import AsyncGenerator, override

from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.genai import types  # noqa
from mtmai.mtlibs.mtfs import get_s3fs

# from mtmai.tts import voice
from mtmai.NarratoAI.services import subtitle, voice


async def generate_audio(
    output_audio_file,
    voice_rate=1.0,
    voice_name="zh-CN-XiaoxiaoNeural",
    video_script="",
):
    sub_maker = await voice.tts_edgetts(
        text=video_script,
        voice_name=voice.parse_voice_name(voice_name),
        # voice_rate=voice_rate,
        voice_file=output_audio_file,
    )
    if sub_maker is None:
        raise ValueError("failed to generate audio, sub_maker is None")

    audio_duration = math.ceil(voice.get_audio_duration(sub_maker))
    return output_audio_file, audio_duration, sub_maker


def generate_subtitle(
    subtitle_output_path, video_script, sub_maker, audio_file, subtitle_provider="edge"
):
    """
    生成字幕
    """
    subtitle_fallback = False
    if subtitle_provider == "edge":
        voice.create_subtitle(
            text=video_script, sub_maker=sub_maker, subtitle_file=subtitle_output_path
        )
        if not os.path.exists(subtitle_output_path):
            subtitle_fallback = True
            raise ValueError("failed to generate subtitle")

    if subtitle_provider == "whisper" or subtitle_fallback:
        subtitle.create(audio_file=audio_file, subtitle_file=subtitle_output_path)
        subtitle.correct(subtitle_file=subtitle_output_path, video_script=video_script)

    return subtitle.file_to_subtitles(subtitle_output_path)


class AudioGenAgent(BaseAgent):
    """
    根据最终的视频生成参数, 合并生成最终的视频
    """

    model_config = {"arbitrary_types_allowed": True}

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        output_dir = ctx.session.state["output_dir"]
        # 生成 音频讲解
        audio_file, audio_duration, sub_maker = await generate_audio(
            output_audio_file=path.join(output_dir, "audio.mp3"),
            video_script=ctx.session.state["video_script"],
        )

        if not audio_file:
            yield Event(
                author=ctx.agent.name,
                content=types.Content(
                    role="assistant",
                    parts=[types.Part(text="音频生成失败")],
                ),
            )
            return

        # 上传
        get_s3fs().upload_file(audio_file, f"short_videos/audio-{ctx.session.id}.mp3")
        yield Event(
            author=ctx.agent.name,
            content=types.Content(
                role="assistant",
                parts=[types.Part(text="音频生成成功")],
            ),
            actions={
                "state_delta": {
                    "audio_file": audio_file,
                    "audio_duration": audio_duration,
                },
                "artifact_delta": {
                    "audio.mp3": 2,
                    "subtitle.srt": 2,
                },
            },
        )

        # 生成字幕
        subtitle_path = path.join(output_dir, "subtitle.srt")
        subtitle = generate_subtitle(
            subtitle_output_path=subtitle_path,
            video_script=ctx.session.state["video_script"],
            sub_maker=sub_maker,
            audio_file=audio_file,
        )
        if not subtitle:
            raise ValueError("failed to generate subtitle")

        yield Event(
            author=ctx.agent.name,
            content=types.Content(
                role="assistant",
                parts=[types.Part(text="字幕生成成功")],
            ),
            actions={
                "state_delta": {
                    "subtitle": subtitle,
                    "subtitle_path": subtitle_path,
                },
            },
        )
