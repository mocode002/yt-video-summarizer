import logging
from config import get_gemini_client
from transcript import get_transcript

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

def summarize_video(url: str, model: str = "gemini-2.5-flash",style: str = "summary", verbose: bool = False) -> str:
    client = get_gemini_client()

    try:
        transcript = get_transcript(url)
        if verbose:
            logging.info("Transcript successfully fetched.")
    except Exception as e:
        raise RuntimeError(f"Error fetching transcript: {e}")

    prompt = build_summary_prompt(transcript, style)

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
