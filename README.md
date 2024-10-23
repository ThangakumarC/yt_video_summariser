# YouTube Transcript to Detailed Notes Converter

This project is a Streamlit-based web application that extracts transcripts from YouTube videos, summarizes them using Google's Generative AI, and stores the summaries in a local SQLite database. It also allows users to view and delete past summaries.

## Features
- Extracts transcript from YouTube videos using the `youtube_transcript_api`.
- Summarizes the video transcript using Google's Generative AI (`gemini-pro`).
- Automatically generates an engaging video title based on the transcript.
- Stores generated summaries in an SQLite database for future reference.
- Allows users to view and delete summaries from the database.
- User-friendly interface built with Streamlit.
