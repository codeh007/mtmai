# import os.path
# from os import path

# from loguru import logger
# from mtmai.mpt.config import config
# from mtmai.mpt.models.schema import VideoConcatMode
# from mtmai.mpt.services import material, subtitle, video
# from mtmai.tts import voice
# from mtmai.tts.tts import generate_audio


# def generate_subtitle(output_dir, params, video_script, sub_maker, audio_file):
#     if not params.subtitle_enabled:
#         return ""

#     subtitle_path = path.join(output_dir, "subtitle.srt")
#     subtitle_provider = config.app.get("subtitle_provider", "").strip().lower()
#     logger.info(f"\n\n## generating subtitle, provider: {subtitle_provider}")

#     subtitle_fallback = False
#     if subtitle_provider == "edge":
#         voice.create_subtitle(
#             text=video_script, sub_maker=sub_maker, subtitle_file=subtitle_path
#         )
#         if not os.path.exists(subtitle_path):
#             subtitle_fallback = True
#             raise ValueError("failed to generate subtitle")

#     if subtitle_provider == "whisper" or subtitle_fallback:
#         subtitle.create(audio_file=audio_file, subtitle_file=subtitle_path)
#         subtitle.correct(subtitle_file=subtitle_path, video_script=video_script)

#     subtitle_lines = subtitle.file_to_subtitles(subtitle_path)
#     if not subtitle_lines:
#         raise ValueError("failed to generate subtitle")

#     return subtitle_path


# def get_video_materials(output_dir, params, video_terms, audio_duration):
#     downloaded_videos = material.download_videos(
#         output_dir=output_dir,
#         search_terms=video_terms,
#         source=params.video_source,
#         video_aspect=params.video_aspect,
#         video_contact_mode=params.video_concat_mode,
#         audio_duration=audio_duration * params.video_count,
#         max_clip_duration=params.video_clip_duration,
#     )
#     return downloaded_videos


# def generate_final_videos(
#     output_dir, params, downloaded_videos, audio_file, subtitle_path
# ):
#     final_video_paths = []
#     combined_video_paths = []
#     video_concat_mode = (
#         params.video_concat_mode if params.video_count == 1 else VideoConcatMode.random
#     )
#     video_transition_mode = params.video_transition_mode

#     _progress = 50
#     for i in range(params.video_count):
#         index = i + 1
#         combined_video_path = path.join(output_dir, f"combined-{index}.mp4")
#         logger.info(f"\n\n## combining video: {index} => {combined_video_path}")
#         video.combine_videos(
#             combined_video_path=combined_video_path,
#             video_paths=downloaded_videos,
#             audio_file=audio_file,
#             video_aspect=params.video_aspect,
#             video_concat_mode=video_concat_mode,
#             video_transition_mode=video_transition_mode,
#             max_clip_duration=params.video_clip_duration,
#             threads=params.n_threads,
#         )

#         # _progress += 50 / params.video_count / 2
#         # sm.state.update_task(task_id, progress=_progress)

#         final_video_path = path.join(output_dir, f"final-{index}.mp4")

#         logger.info(f"\n\n## generating video: {index} => {final_video_path}")
#         video.generate_video(
#             video_path=combined_video_path,
#             audio_path=audio_file,
#             subtitle_path=subtitle_path,
#             output_file=final_video_path,
#             params=params,
#         )

#         # _progress += 50 / params.video_count / 2
#         # sm.state.update_task( progress=_progress)

#         final_video_paths.append(final_video_path)
#         combined_video_paths.append(combined_video_path)

#     return final_video_paths, combined_video_paths


# async def start_gen_video(output_dir, params: dict, stop_at: str = "video"):
#     # if isinstance(params.get("video_concat_mode"), str):
#     #     params.video_concat_mode = VideoConcatMode(params.video_concat_mode)

#     # 3. Generate audio
#     audio_file, audio_duration, sub_maker = await generate_audio(
#         output_dir, params, params.get("video_script")
#     )
#     if not audio_file:
#         raise ValueError("failed to generate audio")

#     if stop_at == "audio":
#         return {"audio_file": audio_file, "audio_duration": audio_duration}

#     # 4. Generate subtitle
#     subtitle_path = generate_subtitle(
#         output_dir, params, params.get("video_script"), sub_maker, audio_file
#     )

#     if stop_at == "subtitle":
#         return {"subtitle_path": subtitle_path}

#     # 5. Get video materials
#     downloaded_videos = get_video_materials(
#         output_dir, params, params.video_terms, audio_duration
#     )
#     if not downloaded_videos:
#         raise ValueError("failed to get video materials")

#     # 6. Generate final videos
#     final_video_paths, combined_video_paths = generate_final_videos(
#         output_dir, params, downloaded_videos, audio_file, subtitle_path
#     )

#     return {
#         "videos": final_video_paths,
#         "combined_videos": combined_video_paths,
#         "audio_file": audio_file,
#         "audio_duration": audio_duration,
#         "subtitle_path": subtitle_path,
#         "materials": downloaded_videos,
#     }
