from Components.Edit import crop_video, extractAudio
from Components.FaceCrop import combine_videos, crop_to_vertical
from Components.LanguageTasks import GetHighlight
from Components.Transcription import transcribeAudio
from Components.YoutubeDownloader import download_youtube_video

# url = input("Enter YouTube video URL: ")

url = "https://www.youtube.com/shorts/HuoeOkoF3T0"
Vid = download_youtube_video(url)
if Vid:
    Vid = Vid.replace(".webm", ".mp4")
    print(f"Downloaded video and audio files successfully! at {Vid}")

    Audio = extractAudio(Vid)
    if Audio:
        transcriptions = transcribeAudio(Audio)
        if len(transcriptions) > 0:
            TransText = ""

            for text, start, end in transcriptions:
                TransText += f"{start} - {end}: {text}"

            start, stop = GetHighlight(TransText)
            if start != 0 and stop != 0:
                print(f"Start: {start} , End: {stop}")

                Output = "Out.mp4"

                crop_video(Vid, Output, start, stop)
                croped = "croped.mp4"

                crop_to_vertical("Out.mp4", croped)
                combine_videos("Out.mp4", croped, "Final.mp4")
            else:
                print("Error in getting highlight")
        else:
            print("No transcriptions found")
    else:
        print("No audio file found")
else:
    print("Unable to Download the video")
