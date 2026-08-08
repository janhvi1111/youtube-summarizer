import os
import re
import traceback
from flask import Flask, request, jsonify  # type: ignore
from flask_cors import CORS  # type: ignore
from google import genai  # Modern Gemini SDK
from google.genai import errors as genai_errors
from youtube_transcript_api import (  # type: ignore
    YouTubeTranscriptApi,
    TranscriptsDisabled,
    NoTranscriptFound,
)

try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv()
except ImportError:
    pass

# --------------------------
# App & Gemini Setup
# --------------------------
app = Flask(__name__)
CORS(app)

# Initialize Gemini Client (uses GEMINI_API_KEY from environment)
client = genai.Client()

# Recommended fast model for text tasks
MODEL_ID = "gemini-3.6-flash"


# --------------------------
# Helper Functions
# --------------------------
def get_summary(text_content):
    """Sends prompt content to Gemini API and returns generated summary text."""
    prompt = f"""
You are an expert video content summarizer.

Summarize the following YouTube video transcript into:
- Simple, engaging language
- Clear bullet points
- Important concepts and key takeaways only

Transcript Content:
{text_content}
"""
    try:
        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )
        return response.text
    except genai_errors.APIError as e:
        if e.code == 429:
            raise Exception("Rate limit reached. Please wait a few seconds and try again.")
        raise Exception(f"Gemini API Error: {e.message}")


def extract_video_id(url):
    """Extracts 11-character YouTube video ID from various URL formats."""
    patterns = [
        r"v=([a-zA-Z0-9_-]{11})",
        r"youtu\.be/([a-zA-Z0-9_-]{11})",
        r"youtube\.com/shorts/([a-zA-Z0-9_-]{11})",
        r"youtube\.com/embed/([a-zA-Z0-9_-]{11})"
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)

    return None


# --------------------------
# YouTube Summarizer Endpoint
# --------------------------
@app.route("/summarize/youtube", methods=["POST"])
def summarize_youtube():
    try:
        data = request.get_json() or {}
        url = data.get("url", "").strip()

        if not url:
            return jsonify({"error": "Please enter a YouTube URL."}), 400

        video_id = extract_video_id(url)
        if not video_id:
            return jsonify({"error": "Invalid YouTube URL format."}), 400

        # Fetch transcript
        ytt_api = YouTubeTranscriptApi()

        try:
            transcript = ytt_api.fetch(video_id, languages=["en"])
        except (NoTranscriptFound, Exception):
            try:
                transcript_list = ytt_api.list(video_id)
                transcript = next(iter(transcript_list)).fetch()
            except TranscriptsDisabled:
                return jsonify({"error": "Transcripts are disabled for this YouTube video."}), 400
            except Exception:
                return jsonify({"error": "No transcripts or captions available for this video."}), 400

        # Combine transcript text segments
        transcript_text = " ".join(item.text for item in transcript)

        if not transcript_text.strip():
            return jsonify({"error": "Transcript was empty."}), 400

        summary = get_summary(transcript_text)
        return jsonify({"summary": summary})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# --------------------------
# AI Chatbot Endpoint
# --------------------------
@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json() or {}
        user_message = data.get("message", "").strip()
        context = data.get("context", "").strip()

        if not user_message:
            return jsonify({"error": "Message cannot be empty."}), 400

        # Include context if a summary exists
        if context:
            prompt = f"Context from YouTube Video Summary:\n{context}\n\nUser Question: {user_message}"
        else:
            prompt = user_message

        response = client.models.generate_content(
            model=MODEL_ID,
            contents=prompt
        )

        return jsonify({"response": response.text})

    except Exception as e:
        traceback.print_exc()
        return jsonify({"error": str(e)}), 500


# --------------------------
# Run App
# --------------------------
if __name__ == "__main__":
    app.run(debug=True)