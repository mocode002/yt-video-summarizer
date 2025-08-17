import logging
from config import get_gemini_client
from transcript import get_transcript
from cache import redis_client, generate_summary_cache_key, generate_transcript_cache_key

STYLE_PROMPTS = {
    "summary": "Summarize the following YouTube video transcript:",
    "tldr": "Give a TL;DR (too long; didn't read) summary of the following YouTube video transcript:",
    "bullets": "Summarize the following YouTube video transcript in concise bullet points:",
    "eli5": "Explain the following YouTube video transcript like I'm 5 years old:"
}

def build_summary_prompt(transcript: str, style: str = "summary") -> str:
    if style not in STYLE_PROMPTS:
        logging.warning(f"Style '{style}' not recognized. Using default 'summary'.")
        style = "summary"
    return f"You are a helpful assistant. {STYLE_PROMPTS[style]}\n\n{transcript}"

def summarize_video(
        url: str,
        model: str = "gemini-2.5-flash",
        style: str = "summary",
        verbose: bool = False
    ) -> tuple[str, str]:

    summary_cache_key = generate_summary_cache_key(url, model, style)
    transcript_cache_key = generate_transcript_cache_key(url)

    # Check Redis cache for transcript
    cached_transcript = redis_client.get(transcript_cache_key)
    if cached_transcript :
        transcript = cached_transcript.decode()
    else :
        try:
            transcript = get_transcript(url)
            if verbose:
                logging.info("Transcript successfully fetched.")
            # Cache transcript in Redis (24h)
            redis_client.setex(transcript_cache_key, 24*3600, transcript)
        except Exception as e:
            raise RuntimeError(f"Error fetching transcript: {e}")
        
    # Check Redis cache for summary
    cached_summary = redis_client.get(summary_cache_key)   
    if cached_summary:
        if verbose:
            logging.info("Returning cached summary from Redis.")
        summary = cached_summary.decode()
        return summary, transcript


    client = get_gemini_client()
    prompt = build_summary_prompt(transcript, style)

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )

        summary = response.text

        # Cache summary in Redis (24h)
        redis_client.setex(summary_cache_key, 24*3600, summary)

        if verbose:
            logging.info("Summary successfully generated.")
        return summary, transcript
    except Exception as e:
        raise RuntimeError(f"Error generating summary: {e}")
