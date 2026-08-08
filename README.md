# YouTube AI Summarizer + Chatbot 🎥🤖

An AI-powered web application that summarizes YouTube videos and allows users to ask questions about the video summary using an AI chatbot.

## 📌 Project Overview

This project takes a YouTube video URL, extracts its transcript, and uses Google's Gemini AI to generate a simple and easy-to-understand summary.

After getting the summary, users can interact with the AI chatbot and ask questions about the video.

## ✨ Features

- 🎥 YouTube video URL processing
- 📝 Automatic transcript extraction
- 🤖 AI-powered video summarization
- 📌 Clear bullet-point summaries
- 💬 AI chatbot for asking questions
- 🧠 Chatbot can use the generated video summary as context
- ⚡ React-based user interface
- 🔗 Flask backend API
- 📱 CORS-enabled frontend/backend communication

## 🛠️ Technologies Used

### Frontend

- React
- Axios
- React Markdown
- JavaScript
- HTML
- CSS

### Backend

- Python
- Flask
- Flask-CORS
- Google Gemini API
- YouTube Transcript API
- python-dotenv

## 📁 Project Structure

```text
AI SUMMARIZER/
│
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   └── package-lock.json
│
├── backend/
│   ├── app.py
│   ├── requirements.txt
│
└── README.md
