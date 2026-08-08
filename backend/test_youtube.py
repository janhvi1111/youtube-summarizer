from youtube_transcript_api import YouTubeTranscriptApi

video_id = "qaPMdcCqtWk"

try:
    api = YouTubeTranscriptApi()
    transcript = api.fetch(video_id)

    print("SUCCESS!")
    print(transcript[:3])

except Exception as e:
    import traceback
    traceback.print_exc()