import math
from os import path

# from mtmai.mpt.models import const
# from mtmai.mpt.services import state as sm
from mtmai.tts import voice

# from loguru import logger


async def generate_audio(
    output_dir, voice_rate=1.0, voice_name="zh-CN-XiaoxiaoNeural", video_script=""
):
    # logger.info("\n\n## generating audio")
    audio_file = path.join(output_dir, "audio.mp3")
    sub_maker = await voice.tts(
        text=video_script,
        voice_name=voice.parse_voice_name(voice_name),
        voice_rate=voice_rate,
        voice_file=audio_file,
    )
    if sub_maker is None:
        # sm.state.update_task(task_id, state=const.TASK_STATE_FAILED)
        # logger.error("""failed to generate audio""".strip())
        # return None, None, None
        raise ValueError("failed to generate audio, sub_maker is None")

    audio_duration = math.ceil(voice.get_audio_duration(sub_maker))
    return audio_file, audio_duration, sub_maker
