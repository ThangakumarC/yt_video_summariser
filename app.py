import streamlit as st
from dotenv import load_dotenv
import os
import google.generativeai as genai
from youtube_transcript_api import YouTubeTranscriptApi
from database import save_summary_to_db, get_summaries_from_db, delete_summary_from_db

load_dotenv()  # Load environment variables
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Prompt for summarization
summary_prompt = """You are a YouTube video summarizer. You will be taking the transcript text and summarizing the entire video 
and providing the important summary in points within 600 words. Please provide the summary of the text given here."""

# Prompt for title generation
title_prompt = """You are a title generator. Given the following transcript of a YouTube video, create a suitable and engaging title for it:
"""

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
def generate_summary(transcript_text):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(summary_prompt + transcript_text)
    return response.text

# Function to generate title from transcript
def generate_title(transcript_text):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(title_prompt + transcript_text)
    return response.text

# Streamlit app setup
st.title("YouTube Transcript to Detailed Notes Converter")

youtube_link = st.text_input("Enter YouTube Video Link:")

if youtube_link:
    video_id = youtube_link.split("=")[1]
    st.image(f"http://img.youtube.com/vi/{video_id}/0.jpg", use_column_width=True)

if st.button("Summarize"):
    transcript_text, video_id = extract_transcript_details(youtube_link)
    if transcript_text and video_id:
        summary = generate_summary(transcript_text)
        title = generate_title(transcript_text)

        st.markdown("## Title:")
        st.write(title)

        st.markdown("## Detailed Notes:")
        st.write(summary)

        # Save the summary with the automatically generated title
        save_summary_to_db(video_id, title, transcript_text, summary)

# Initialize session state for summaries
if "summaries" not in st.session_state:
    st.session_state.summaries = get_summaries_from_db()

# Initialize session state for history visibility
if "show_history" not in st.session_state:
    st.session_state.show_history = False  # Start with history hidden

# Button to toggle history visibility
if st.button("Show History"):
    st.session_state.show_history = not st.session_state.show_history

# Display history section based on visibility state
if st.session_state.show_history:
    st.markdown("## History")
    summaries = st.session_state.summaries

    if summaries:
        for summary in summaries:
            with st.expander(f"Video Title: {summary[2]}"):
                st.markdown(f"**Generated on**: {summary[5]}")
                # Button to view the summary
                if st.button(f"View Summary", key=f"view_{summary[0]}"):
                    st.markdown("## Summary:")
                    st.write(summary[4])

                # Button to delete the summary
                if st.button(f"Delete Summary", key=f"delete_{summary[0]}"):
                    delete_summary_from_db(summary[0])  # Delete from the database
                    st.success(f"Deleted summary of {summary[2]}")

                    # Refresh the displayed summaries
                    st.session_state.summaries = get_summaries_from_db()  # Fetch updated summaries
    else:
        st.write("No history available.")
