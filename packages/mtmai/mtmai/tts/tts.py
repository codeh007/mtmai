import math
from os import path

from loguru import logger

# from mtmai.mpt.models import const
# from mtmai.mpt.services import state as sm
from mtmai.mtlibs.mpt_utils import mpt_utils as utils
from mtmai.tts import voice


async def generate_audio(task_id, params, video_script):
    logger.info("\n\n## generating audio")
    audio_file = path.join(utils.task_dir(task_id), "audio.mp3")
    sub_maker = await voice.tts(
        text=video_script,
        voice_name=voice.parse_voice_name(params.voice_name),
        voice_rate=params.voice_rate,
        voice_file=audio_file,
    )
    if sub_maker is None:
        # sm.state.update_task(task_id, state=const.TASK_STATE_FAILED)
        logger.error("""failed to generate audio""".strip())
        return None, None, None

    audio_duration = math.ceil(voice.get_audio_duration(sub_maker))
    return audio_file, audio_duration, sub_maker
