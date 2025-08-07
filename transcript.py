from urllib.parse import urlparse, parse_qs
from youtube_transcript_api import YouTubeTranscriptApi

def get_transcript(url):
    query = urlparse(url).query
    video_id = parse_qs(query).get('v', [None])[0]

    ytt_api = YouTubeTranscriptApi()
    fetched_transcript = ytt_api.fetch(video_id)

    transcript = ' '.join(snippet.text.strip() for snippet in fetched_transcript)
    return transcript