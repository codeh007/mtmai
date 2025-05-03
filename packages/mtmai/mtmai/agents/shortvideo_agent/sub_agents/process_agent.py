from google.adk.agents import SequentialAgent
from google.genai import types  # noqa
from mtmai.agents.shortvideo_agent.sub_agents.audio_agent import AudioGenAgent
from mtmai.agents.shortvideo_agent.sub_agents.materials_agent import MaterialsAgent
from mtmai.agents.shortvideo_agent.sub_agents.videoscript_agent import (
    new_videoscript_agent,
)
from mtmai.agents.shortvideo_agent.sub_agents.videosuject_agent import (
    new_video_subject_agent,
)

from .finnal_gen_video import FinalGenVideoAgent
from .video_terms_agent import new_video_terms_agent


def new_video_process_agent():
    """
    按照顺序执行各个子任务, 完成视频的生成
    """
    sequential_agent = SequentialAgent(
        name="ShortvideoProcessing",
        sub_agents=[
            new_video_subject_agent(),
            new_videoscript_agent(),
            new_video_terms_agent(),
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
    )
    return sequential_agent
