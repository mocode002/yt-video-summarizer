from config import get_gemini_client
from transcript import get_transcript
import argparse
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def build_summary_prompt(transcript: str) -> str:
    # prompt = f"Summarize the following YouTube video transcript:\n\n{transcript}"
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
        return response.text
    except Exception as e:
        raise RuntimeError(f"Error generating summary: {e}")

def main():
    test_url = 'https://www.youtube.com/watch?v=ji8F8ppY8bs'

    parser = argparse.ArgumentParser(description="YouTube Transcript Summarizer with Gemini")

    parser.add_argument("--url", required=False, help="YouTube video URL")
    parser.add_argument("--model", default="gemini-2.5-flash", help="Gemini model to use")
    parser.add_argument("--output", help="Optional path to save summary to .txt file")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)


    if args.url:
        input_url = args.url
    else:
        input_url = test_url

    try:
        summuary = summarize_video(input_url, model=args.model, verbose=args.verbose)
        print("\nSummary:\n", summuary)

        if args.output:
            with open(args.output, "w") as f:
                f.write(summuary)
            logging.info(f"Summary saved to: {args.output}")


    except Exception as e:
        logging.error(e)

if __name__ == "__main__":
    main()