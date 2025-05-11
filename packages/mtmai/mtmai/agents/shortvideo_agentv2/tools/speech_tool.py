"""音频生成工具"""

import logging
import math
import os
from os import path

from google.adk.tools import ToolContext
from google.genai import types  # noqa
from mtmai.NarratoAI.services import subtitle, voice

logger = logging.getLogger(__name__)


async def speech_tool(script: str, tool_context: ToolContext):
    """
    根据脚本生成音频及其对应的字幕
    args:
        script: 脚本
        tool_context: 工具上下文
    """
    try:
        output_dir = tool_context.state["output_dir"]
        # 生成 音频讲解
        voice_name = tool_context.state["voice_name"]
        output_audio_file = path.join(output_dir, "audio.mp3")
        sub_maker = await voice.tts_edgetts(
            text=script,
            voice_name=voice.parse_voice_name(voice_name),
            # voice_rate=voice_rate,
            voice_file=output_audio_file,
        )
        if sub_maker is None:
            return (
                f"音频生成失败, 音频文件: 输出文件不存在, 文件路径: {output_audio_file}"
            )

        audio_duration = math.ceil(voice.get_audio_duration(sub_maker))

        if not output_audio_file:
            return (
                f"音频生成失败, 音频文件: 输出文件不存在, 文件路径: {output_audio_file}"
            )
        tool_context.state["audio_duration"] = audio_duration
        tool_context.state["audio_file"] = output_audio_file
        # 上传
        audio_file_bytes = open(output_audio_file, "rb").read()
        mp3_part = types.Part(
            inline_data=types.Blob(data=audio_file_bytes, mime_type="audio/mpeg")
        )

        await tool_context.save_artifact("speech.mp3", mp3_part)
        # 生成字幕

        subtitle_fallback = False
        subtitle_path = path.join(output_dir, "subtitle.srt")
        subtitle_provider = tool_context.state["voice_llm_provider"]
        if subtitle_provider == "edgetts":
            voice.create_subtitle(
                text=script, sub_maker=sub_maker, subtitle_file=subtitle_path
            )
            if not os.path.exists(subtitle_path):
                subtitle_fallback = True
                return (
                    f"字幕生成失败, 字幕文件: 输出文件不存在, 文件路径: {subtitle_path}"
                )

        elif subtitle_provider == "whisper" or subtitle_fallback:
            subtitle.create(audio_file=output_audio_file, subtitle_file=subtitle_path)
            subtitle.correct(subtitle_file=subtitle_path, video_script=script)

        else:
            return f"字幕生成失败, 未知字幕提供者: {subtitle_provider}"

        subtitle_srt = subtitle.file_to_subtitles(subtitle_path)

        if not subtitle_srt:
            return f"字幕生成失败, 字幕文件: 输出文件不存在, 文件路径: {subtitle_path}"
        tool_context.state["subtitle_path"] = subtitle_path

        subtitle_file_bytes = open(subtitle_path, "rb").read()
        srt_part = types.Part(
            inline_data=types.Blob(data=subtitle_file_bytes, mime_type="text/plain")
        )
        await tool_context.save_artifact("subtitle.srt", srt_part)
        return f"生成音频及其对应的字幕完成, 音频文件: {output_audio_file}, 字幕文件: {subtitle_path}, 音频时长: {audio_duration} 秒"
    except Exception as e:
        logger.exception(e)
        return f"音频生成失败, 错误信息: {e}"
