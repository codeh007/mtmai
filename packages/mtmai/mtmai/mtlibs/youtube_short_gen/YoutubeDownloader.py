import logging
import os

import ffmpeg
from pytubefix import YouTube

logger = logging.getLogger(__name__)


def get_video_size(stream):
  return stream.filesize / (1024 * 1024)


def download_youtube_video(url, output_dir=".vol/_youtube_videos_cache"):
  yt = YouTube(url)

  video_streams = yt.streams.filter(type="video").order_by("resolution").desc()
  audio_stream = yt.streams.filter(only_audio=True).first()

  # logger.info("Available video streams:")
  for i, stream in enumerate(video_streams):
    size = get_video_size(stream)
    stream_type = "Progressive" if stream.is_progressive else "Adaptive"
    logger.info(f"{i}. Resolution: {stream.resolution}, Size: {size:.2f} MB, Type: {stream_type}")

  #   choice = int(input("Enter the number of the video stream to download: "))
  choice = 0
  selected_stream = video_streams[choice]

  if not os.path.exists(output_dir):
    os.makedirs(output_dir)

  # logger.info(f"Downloading video: {yt.title}")
  video_file = selected_stream.download(output_path=output_dir, filename_prefix="video_")

  if not selected_stream.is_progressive:
    # logger.info("Downloading audio...")
    audio_file = audio_stream.download(output_path=output_dir, filename_prefix="audio_")

    # logger.info("Merging video and audio...")
    output_file = os.path.join(output_dir, f"{yt.title}.mp4")

    stream = ffmpeg.input(video_file)
    audio = ffmpeg.input(audio_file)
    stream = ffmpeg.output(
      stream,
      audio,
      output_file,
      vcodec="libx264",
      acodec="aac",
      strict="experimental",
    )
    ffmpeg.run(stream, overwrite_output=True)

    os.remove(video_file)
    os.remove(audio_file)
  else:
    output_file = video_file

  # logger.info(f"Downloaded: {yt.title} to {output_dir} folder, file path: {output_file}")
  return yt
