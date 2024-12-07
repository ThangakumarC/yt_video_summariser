import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from database import save_summary_to_db, get_summaries_from_db, delete_summary_from_db

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Streamlit app setup
st.title("YouTube Transcript to Detailed Notes Converter")

# Prompt adjustments for summary size
def get_summary_prompt(length):
    if length == "Small":
        return """You are a YouTube video summarizer. Summarize the video into a key points summary in less than 100 words."""
    elif length == "Medium":
        return """You are a YouTube video summarizer. Summarize the video into a moderate summary in 200–300 words, highlighting the main points with subheadings."""
    elif length == "Large":
        return """You are a YouTube video summarizer. Provide a detailed summary of 500–600 words, covering all key aspects of the video."""
    return ""  # Default case


# Function to extract transcript from YouTube video
def extract_transcript_details(youtube_video_url):
    try:
        video_id = youtube_video_url.split("=")[1]
        transcript_text = YouTubeTranscriptApi.get_transcript(video_id)

        transcript = ""
        for i in transcript_text:
            transcript += " " + i["text"]

        return transcript, video_id
    except Exception as e:
        st.error(f"Error extracting transcript: {e}")
        return None, None

# Function to generate summary from transcript
def generate_summary(transcript_text, length):
    prompt = get_summary_prompt(length) + f" {transcript_text}"
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# Function to generate title from transcript
def generate_title(transcript_text):
    title_prompt = """You are a title generator. Given the following transcript of a YouTube video, create a suitable and engaging title for it with a four to five words:
    """
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(title_prompt + transcript_text)
    return response.text

# User input for YouTube link
youtube_link = st.text_input("Enter YouTube Video Link:", key="youtube_link_input")

# Display video thumbnail if link is provided
if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

# Add buttons for summary length
st.markdown("### Select Summary Length")
summary_length = st.radio("Choose summary size:", ["Small", "Medium", "Large"], key="summary_size_selector")

# When the "Summarize" button is clicked
if st.button("Summarize", key="summarize_button"):
    transcript_text, video_id = extract_transcript_details(youtube_link)
    if transcript_text and video_id:
        summary = generate_summary(transcript_text, summary_length)
        title = generate_title(transcript_text)

        st.markdown("## Title:")
        st.write(title)

        st.markdown("## Summary:")
        st.write(summary)

        # Save to database
        save_summary_to_db(video_id, title, transcript_text, summary)

# Initialize session state for summaries
if "summaries" not in st.session_state:
    st.session_state.summaries = get_summaries_from_db()

# Initialize session state for history visibility
if "show_history" not in st.session_state:
    st.session_state.show_history = False  # Start with history hidden

# Button to toggle history visibility
if st.button("Show History", key="show_history_button"):
    st.session_state.show_history = not st.session_state.show_history

# Display history section based on visibility state
if st.session_state.show_history:
    st.markdown("## History")
    summaries = st.session_state.summaries

    if summaries:
        for summary in summaries:
            with st.expander(f"Video Title: {summary[2]}"):
                st.markdown(f"**Generated on**: {summary[5]}")
                
                # View Summary button with unique key
                if st.button(f"View Summary {summary[0]}", key=f"view_{summary[0]}"):
                    st.markdown("## Summary:")
                    st.write(summary[4])

                # Delete Summary button with unique key
                if st.button(f"Delete Summary {summary[0]}", key=f"delete_{summary[0]}"):
                    delete_summary_from_db(summary[0])  # Delete from the database
                    st.success(f"Deleted summary of {summary[2]}")

                    # Refresh the displayed summaries
                    st.session_state.summaries = get_summaries_from_db()  # Fetch updated summaries
    else:
        st.write("No history available.")
