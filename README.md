# YouTube Video Summarizer with Gemini AI

This project summarizes YouTube video transcripts using Google's Gemini AI models.  
It fetches transcripts, summarizes them with different styles, and offers a simple Streamlit UI.

---

## Features

- Fetches transcript of any YouTube video (public transcripts)
- Supports Gemini AI models (`gemini-2.5-flash`, `gemini-1.5-flash`, etc.)
- Streamlit UI for easy interaction and summary download
- Summarizes transcript with customizable styles (Summary, TL;DR, Bullet points, ELI5)
- Caching for repeated video summaries to reduce API calls (planned)
- Displays video title and thumbnail via YouTube Data API (planned)

---

## Getting Started

### Prerequisites

- Python 3.9+
- [Google Gemini API credentials](https://cloud.google.com/genai)
- (Optional) YouTube Data API key to display video info

### Installation

```bash
git clone https://github.com/mocode002/yt-video-summarizer.git
cd yt-video-summarizer
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
```
### Usage

#### Command Line

```bash
python main.py --url "https://www.youtube.com/watch?v=VIDEO_ID" --model "gemini-2.5-flash" --output "summary.txt" --verbose
```


#### Streamlit UI

```bash
streamlit run app.py
```

----------

## Environment Variables

Create a `.env` file or set environment variables:

```bash
GEMINI_API_KEY=your_google_gemini_api_key
```

----------

## License

MIT License

----------

## Acknowledgments

-   [Google Gemini](https://cloud.google.com/genai)
     
-   [Streamlit](https://streamlit.io/)