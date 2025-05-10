from enum import Enum
from typing import Any, List, Optional

import pydantic
from pydantic import BaseModel, Field

PUNCTUATIONS = [
    "?",
    ",",
    ".",
    "、",
    ";",
    ":",
    "!",
    "…",
    "？",
    "，",
    "。",
    "、",
    "；",
    "：",
    "！",
    "...",
]

TASK_STATE_FAILED = -1
TASK_STATE_COMPLETE = 1
TASK_STATE_PROCESSING = 4

FILE_TYPE_VIDEOS = ["mp4", "mov", "mkv", "webm"]
FILE_TYPE_IMAGES = ["jpg", "jpeg", "png", "bmp"]


class VideoConcatMode(str, Enum):
    random = "random"
    sequential = "sequential"


class VideoAspect(str, Enum):
    landscape = "16:9"
    portrait = "9:16"
    square = "1:1"

    def to_resolution(self):
        if self == VideoAspect.landscape.value:
            return 1920, 1080
        elif self == VideoAspect.portrait.value:
            return 1080, 1920
        elif self == VideoAspect.square.value:
            return 1080, 1080
        return 1080, 1920


class _Config:
    arbitrary_types_allowed = True


@pydantic.dataclasses.dataclass(config=_Config)
class MaterialInfo:
    provider: str = "pexels"
    url: str = ""
    duration: int = 0


class VideoParams(BaseModel):
    """
    {
      "video_subject": "",
      "video_aspect": "横屏 16:9（西瓜视频）",
      "voice_name": "女生-晓晓",
      "bgm_name": "random",
      "font_name": "STHeitiMedium 黑体-中",
      "text_color": "#FFFFFF",
      "font_size": 60,
      "stroke_color": "#000000",
      "stroke_width": 1.5
    }
    """

    video_subject: str
    video_script: str = ""  # 用于生成视频的脚本
    video_terms: Optional[str | list] = None  # 用于生成视频的关键词
    video_aspect: Optional[VideoAspect] = VideoAspect.portrait.value
    video_concat_mode: Optional[VideoConcatMode] = VideoConcatMode.random.value
    video_clip_duration: Optional[int] = 5
    video_count: Optional[int] = 1

    video_source: Optional[str] = "pexels"
    video_materials: Optional[List[MaterialInfo]] = None  # 用于生成视频的素材

    video_language: Optional[str] = ""  # auto detect

    voice_name: Optional[str] = ""
    voice_volume: Optional[float] = 1.0
    voice_rate: Optional[float] = 1.0
    bgm_type: Optional[str] = "random"
    bgm_file: Optional[str] = ""
    bgm_volume: Optional[float] = 0.2

    subtitle_enabled: Optional[bool] = True
    subtitle_position: Optional[str] = "bottom"  # top, bottom, center
    custom_position: float = 70.0
    font_name: Optional[str] = "STHeitiMedium.ttc"
    text_fore_color: Optional[str] = "#FFFFFF"
    text_background_color: Optional[str] = "transparent"

    font_size: int = 60
    stroke_color: Optional[str] = "#000000"
    stroke_width: float = 1.5
    n_threads: Optional[int] = 2
    paragraph_number: Optional[int] = 1


class SubtitleRequest(BaseModel):
    video_script: str
    video_language: Optional[str] = ""
    voice_name: Optional[str] = "zh-CN-XiaoxiaoNeural-Female"
    voice_volume: Optional[float] = 1.0
    voice_rate: Optional[float] = 1.2
    bgm_type: Optional[str] = "random"
    bgm_file: Optional[str] = ""
    bgm_volume: Optional[float] = 0.2
    subtitle_position: Optional[str] = "bottom"
    font_name: Optional[str] = "STHeitiMedium.ttc"
    text_fore_color: Optional[str] = "#FFFFFF"
    text_background_color: Optional[str] = "transparent"
    font_size: int = 60
    stroke_color: Optional[str] = "#000000"
    stroke_width: float = 1.5
    video_source: Optional[str] = "local"
    subtitle_enabled: Optional[str] = "true"


class AudioRequest(BaseModel):
    video_script: str
    video_language: Optional[str] = ""
    voice_name: Optional[str] = "zh-CN-XiaoxiaoNeural-Female"
    voice_volume: Optional[float] = 1.0
    voice_rate: Optional[float] = 1.2
    bgm_type: Optional[str] = "random"
    bgm_file: Optional[str] = ""
    bgm_volume: Optional[float] = 0.2
    video_source: Optional[str] = "local"


class VideoScriptParams:
    """
    {
      "video_subject": "春天的花海",
      "video_language": "",
      "paragraph_number": 1
    }
    """

    video_subject: Optional[str] = "春天的花海"
    video_language: Optional[str] = ""
    paragraph_number: Optional[int] = 1


class VideoTermsParams:
    """
    {
      "video_subject": "",
      "video_script": "",
      "amount": 5
    }
    """

    video_subject: Optional[str] = "春天的花海"
    video_script: Optional[str] = (
        "春天的花海，如诗如画般展现在眼前。万物复苏的季节里，大地披上了一袭绚丽多彩的盛装。金黄的迎春、粉嫩的樱花、洁白的梨花、艳丽的郁金香……"
    )
    amount: Optional[int] = 5


class BaseResponse(BaseModel):
    status: int = 200
    message: Optional[str] = "success"
    data: Any = None


class TaskVideoRequest(VideoParams, BaseModel):
    pass


class TaskQueryRequest(BaseModel):
    pass


class VideoScriptRequest(VideoScriptParams, BaseModel):
    pass


class VideoTermsRequest(VideoTermsParams, BaseModel):
    pass


######################################################################################################
######################################################################################################
######################################################################################################
######################################################################################################
class TaskResponse(BaseResponse):
    class TaskResponseData(BaseModel):
        task_id: str

    data: TaskResponseData

    class Config:
        json_schema_extra = {
            "example": {
                "status": 200,
                "message": "success",
                "data": {"task_id": "6c85c8cc-a77a-42b9-bc30-947815aa0558"},
            },
        }


class TaskQueryResponse(BaseResponse):
    class Config:
        json_schema_extra = {
            "example": {
                "status": 200,
                "message": "success",
                "data": {
                    "state": 1,
                    "progress": 100,
                    "videos": [
                        "http://127.0.0.1:8080/tasks/6c85c8cc-a77a-42b9-bc30-947815aa0558/final-1.mp4"
                    ],
                    "combined_videos": [
                        "http://127.0.0.1:8080/tasks/6c85c8cc-a77a-42b9-bc30-947815aa0558/combined-1.mp4"
                    ],
                },
            },
        }


class TaskDeletionResponse(BaseResponse):
    class Config:
        json_schema_extra = {
            "example": {
                "status": 200,
                "message": "success",
                "data": {
                    "state": 1,
                    "progress": 100,
                    "videos": [
                        "http://127.0.0.1:8080/tasks/6c85c8cc-a77a-42b9-bc30-947815aa0558/final-1.mp4"
                    ],
                    "combined_videos": [
                        "http://127.0.0.1:8080/tasks/6c85c8cc-a77a-42b9-bc30-947815aa0558/combined-1.mp4"
                    ],
                },
            },
        }


class VideoScriptResponse(BaseResponse):
    class Config:
        json_schema_extra = {
            "example": {
                "status": 200,
                "message": "success",
                "data": {
                    "video_script": "春天的花海，是大自然的一幅美丽画卷。在这个季节里，大地复苏，万物生长，花朵争相绽放，形成了一片五彩斑斓的花海..."
                },
            },
        }


class VideoTermsResponse(BaseResponse):
    class Config:
        json_schema_extra = {
            "example": {
                "status": 200,
                "message": "success",
                "data": {"video_terms": ["sky", "tree"]},
            },
        }


class BgmRetrieveResponse(BaseResponse):
    class Config:
        json_schema_extra = {
            "example": {
                "status": 200,
                "message": "success",
                "data": {
                    "files": [
                        {
                            "name": "output013.mp3",
                            "size": 1891269,
                            "file": "/NarratoAI/resource/songs/output013.mp3",
                        }
                    ]
                },
            },
        }


class BgmUploadResponse(BaseResponse):
    class Config:
        json_schema_extra = {
            "example": {
                "status": 200,
                "message": "success",
                "data": {"file": "/NarratoAI/resource/songs/example.mp3"},
            },
        }


class VideoClipParams(BaseModel):
    """
    NarratoAI 数据模型
    """

    video_clip_json: Optional[list] = Field(
        default=[], description="LLM 生成的视频剪辑脚本内容"
    )
    video_clip_json_path: Optional[str] = Field(
        default="", description="LLM 生成的视频剪辑脚本路径"
    )
    video_origin_path: Optional[str] = Field(default="", description="原视频路径")
    video_aspect: Optional[VideoAspect] = Field(
        default=VideoAspect.portrait.value, description="视频比例"
    )
    video_language: Optional[str] = Field(default="zh-CN", description="视频语言")

    # video_clip_duration: Optional[int] = 5      # 视频片段时长
    # video_count: Optional[int] = 1      # 视频片段数量
    # video_source: Optional[str] = "local"
    # video_concat_mode: Optional[VideoConcatMode] = VideoConcatMode.random.value

    voice_name: Optional[str] = Field(
        default="zh-CN-YunjianNeural", description="语音名称"
    )
    voice_volume: Optional[float] = Field(default=1.0, description="解说语音音量")
    voice_rate: Optional[float] = Field(default=1.0, description="语速")
    voice_pitch: Optional[float] = Field(default=1.0, description="语调")

    bgm_name: Optional[str] = Field(default="random", description="背景音乐名称")
    bgm_type: Optional[str] = Field(default="random", description="背景音乐类型")
    bgm_file: Optional[str] = Field(default="", description="背景音乐文件")

    subtitle_enabled: bool = True
    font_name: str = "SimHei"  # 默认使用黑体
    font_size: int = 36
    text_fore_color: str = "white"  # 文本前景色
    text_back_color: Optional[str] = None  # 文本背景色
    stroke_color: str = "black"  # 描边颜色
    stroke_width: float = 1.5  # 描边宽度
    subtitle_position: str = "bottom"  # top, bottom, center, custom

    n_threads: Optional[int] = Field(
        default=16, description="解说语音音量"
    )  # 线程���，有助于提升视频处理速度

    tts_volume: Optional[float] = Field(
        default=1.0, description="解说语音音量（后处理）"
    )
    original_volume: Optional[float] = Field(default=1.0, description="视频原声音量")
    bgm_volume: Optional[float] = Field(default=0.6, description="背景音乐音量")


class VideoTranscriptionRequest(BaseModel):
    video_name: str
    language: str = "zh-CN"

    class Config:
        arbitrary_types_allowed = True


class VideoTranscriptionResponse(BaseModel):
    transcription: str


class SubtitlePosition(str, Enum):
    TOP = "top"
    CENTER = "center"
    BOTTOM = "bottom"


# 可能没用了
class VideoTransitionMode(str, Enum):
    none = None
    shuffle = "Shuffle"
    fade_in = "FadeIn"
    fade_out = "FadeOut"
    slide_in = "SlideIn"
    slide_out = "SlideOut"


# V2 =======================================================


class GenerateScriptRequest(BaseModel):
    video_path: str
    video_theme: Optional[str] = ""
    custom_prompt: Optional[str] = ""
    skip_seconds: Optional[int] = 0
    threshold: Optional[int] = 30
    vision_batch_size: Optional[int] = 5
    vision_llm_provider: Optional[str] = "gemini"


class GenerateScriptResponse(BaseModel):
    task_id: str
    script: List[dict]


class CropVideoRequest(BaseModel):
    video_origin_path: str
    video_script: List[dict]


class CropVideoResponse(BaseModel):
    task_id: str
    subclip_videos: dict


class DownloadVideoRequest(BaseModel):
    url: str
    resolution: str
    output_format: Optional[str] = "mp4"
    rename: Optional[str] = None


class DownloadVideoResponse(BaseModel):
    task_id: str
    output_path: str
    resolution: str
    format: str
    filename: str


class StartSubclipRequest(BaseModel):
    task_id: str
    video_origin_path: str
    video_clip_json_path: str
    voice_name: Optional[str] = None
    voice_rate: Optional[int] = 0
    voice_pitch: Optional[int] = 0
    subtitle_enabled: Optional[bool] = True
    video_aspect: Optional[str] = "16:9"
    n_threads: Optional[int] = 4
    subclip_videos: list  # 从裁剪视频接口获取的视频片段字典


class StartSubclipResponse(BaseModel):
    task_id: str
    state: str
    videos: Optional[List[str]] = None
    combined_videos: Optional[List[str]] = None
