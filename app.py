import streamlit as st
from config import get_gemini_client
from transcript import get_transcript

st.set_page_config(page_title="🎧 YouTube Video Summarizer", layout="centered")

# UI title
st.title("🎧 YouTube Video Summarizer")
st.markdown("Summarize YouTube videos using Gemini AI and transcripts. Just paste a link below.")

# Input form
with st.form("summarizer_form"):
    url = st.text_input("Enter a YouTube URL", placeholder="https://www.youtube.com/watch?v=...")
    model = st.selectbox("Choose Gemini Model", ["gemini-2.5-flash", "gemini-1.5-flash"])
    verbose = st.checkbox("Verbose (debug info)")
    submitted = st.form_submit_button("Generate Summary")

# Summary generation logic
if submitted:
    if not url:
        st.warning("⚠️ Please enter a valid YouTube URL.")
    else:
        with st.spinner("Fetching transcript and generating summary..."):
            try:
                client = get_gemini_client()
                transcript = get_transcript(url)

                if verbose:
                    st.subheader("📜 Transcript")
                    st.text(transcript[:3000] + "..." if len(transcript) > 3000 else transcript)

                prompt = (
                    "You are a helpful assistant. Summarize the following YouTube video transcript:\n\n"
                    f"{transcript}"
                )

                response = client.models.generate_content(
                    model=model,
                    contents=prompt
                )

                summary = response.text

                st.success("✅ Summary generated!")
                st.subheader("🧠 Summary")
                st.markdown(summary)

                # Download button
                st.download_button(
                    label="💾 Download Summary as .txt",
                    data=summary,
                    file_name="youtube_summary.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"❌ An error occurred: {e}")
