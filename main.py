from summarizer import summarize_video
import argparse
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def main():
    test_url = 'https://www.youtube.com/watch?v=ji8F8ppY8bs'

    parser = argparse.ArgumentParser(description="YouTube Transcript Summarizer with Gemini")

    parser.add_argument("--url", required=False, help="YouTube video URL")
    parser.add_argument("--model", default="gemini-2.5-flash", help="Gemini model to use")
    parser.add_argument("--style", default="summary", choices=["summary", "tldr", "bullets", "eli5"],
                        help="Summary style to use")
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
        summuary = summarize_video(input_url, model=args.model,style=args.style, verbose=args.verbose)[0]
        print("\nSummary:\n", summuary)

        if args.output:
            with open(args.output, "w") as f:
                f.write(summuary)
            logging.info(f"Summary saved to: {args.output}")

    except Exception as e:
        logging.error(e)

if __name__ == "__main__":
    main()