from os import path
from typing import AsyncGenerator, override

from google.adk.agents import BaseAgent
from google.adk.agents.invocation_context import InvocationContext
from google.adk.events import Event
from google.genai import types  # noqa
from loguru import logger
from mtmai.mtlibs.mtfs import get_s3fs
from mtmai.NarratoAI.schema import VideoAspect, VideoConcatMode, VideoTransitionMode
from mtmai.NarratoAI.services import video
from mtmai.NarratoAI.utils import utils


class FinalGenVideoAgent(BaseAgent):
    """
    根据 文案,生成的视频,字幕,素材, 合成最终的视频
    """

    model_config = {"arbitrary_types_allowed": True}

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        output_dir = ctx.session.state["output_dir"]
        final_video_paths = []
        combined_video_paths = []
        video_count = 1
        for i in range(video_count):
            index = i + 1
            combined_video_path = path.join(output_dir, f"combined-{index}.mp4")
            logger.info(f"\n\n## combining video: {index} => {combined_video_path}")
            video.combine_videos(
                combined_video_path=combined_video_path,
                video_paths=ctx.session.state["downloaded_videos"],
                audio_file=ctx.session.state["audio_file"],
                video_aspect=VideoAspect.portrait,
                video_concat_mode=VideoConcatMode.random,
                video_transition_mode=VideoTransitionMode.fade_in,
                max_clip_duration=3,
                threads=2,
            )

            final_video_path = path.join(output_dir, f"final-{index}.mp4")

            logger.info(f"\n\n## generating video: {index} => {final_video_path}")
            font_path = utils.font_dir("MicrosoftYaHeiNormal.ttc")

            # 示例：自定义字幕样式
            subtitle_style = {
                "fontsize": 40,  # 字体大小
                "color": "#ffffff",  # 字体颜色
                "stroke_color": "#000000",  # 描边颜色
                "stroke_width": 1,  # 描边宽度, 范围0-10
                "bg_color": "#000000",  # 半透明黑色背景
                "position": ("bottom", 0.2),  # 距离顶部60%的位置
                "method": "caption",  # 渲染方法
            }

            volume_config = {
                "original": 0.8,  # 原声音量80%
                "bgm": 0.2,  # BGM音量20%
                "narration": 1,  # 解说音量100%
            }

            srt_path = ctx.session.state["subtitle_path"]
            video.generate_video_v3(
                video_path=combined_video_path,
                # audio_path=ctx.session.state["audio_file"],
                # subtitle_path=ctx.session.state["subtitle_path"],
                output_path=final_video_path,
                font_path=font_path,
                subtitle_path=srt_path,
                subtitle_style=subtitle_style,
                volume_config=volume_config,
            )

            final_video_paths.append(final_video_path)
            combined_video_paths.append(combined_video_path)

        # 上传成品视频
        get_s3fs().upload_file(
            final_video_paths[0],
            f"short_videos/final-{ctx.session.id}.mp4",
            "video/mp4",
        )

        yield Event(
            author=ctx.agent.name,
            content=types.Content(
                role="assistant",
                parts=[types.Part(text="视频生成成功")],
            ),
        )
