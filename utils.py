import logging
from config import get_gemini_client
from transcript import get_transcript

def build_summary_prompt(transcript: str) -> str:
    return (
        "You are a helpful assistant. Summarize the following YouTube video transcript:\n\n"
        f"{transcript}"
    )

def summarize_video(url: str, model: str = "gemini-2.5-flash", verbose: bool = False) -> str:
    client = get_gemini_client()

    try:
        transcript = get_transcript(url)
        if verbose:
            logging.info("Transcript successfully fetched.")
    except Exception as e:
        raise RuntimeError(f"Error fetching transcript: {e}")

    prompt = build_summary_prompt(transcript)

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt
        )
        if verbose:
            logging.info("Summary successfully generated.")
        return response.text, transcript
    except Exception as e:
        raise RuntimeError(f"Error generating summary: {e}")
