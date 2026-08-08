import React, { useState } from "react";
import axios from "axios";
import ReactMarkdown from "react-markdown";
import "./App.css";

const API_BASE_URL = process.env.REACT_APP_API_BASE_URL || "http://localhost:5000";

function App() {
  const [youtubeURL, setYoutubeURL] = useState("");
  const [summary, setSummary] = useState("");
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");

  // Chatbot State
  const [chatInput, setChatInput] = useState("");
  const [chatMessages, setChatMessages] = useState([
    { sender: "bot", text: "Hello! Paste a YouTube URL to get a summary, or ask me any question directly." }
  ]);
  const [chatLoading, setChatLoading] = useState(false);

  // Summarize YouTube Video
  const handleSummarize = async () => {
    if (!youtubeURL.trim()) {
      alert("Please enter a YouTube URL.");
      return;
    }

    setLoading(true);
    setSummary("");
    setErrorMessage("");

    try {
      const res = await axios.post(`${API_BASE_URL}/summarize/youtube`, {
        url: youtubeURL,
      });
      setSummary(res.data.summary);
    } catch (err) {
      console.error(err);
      setErrorMessage(
        err.response?.data?.error || "Failed to generate video summary."
      );
    } finally {
      setLoading(false);
    }
  };

  // Chatbot Handler
  const handleSendMessage = async () => {
    if (!chatInput.trim()) return;

    const userMsg = { sender: "user", text: chatInput };
    setChatMessages((prev) => [...prev, userMsg]);
    setChatInput("");
    setChatLoading(true);

    try {
      const res = await axios.post(`${API_BASE_URL}/chat`, {
        message: userMsg.text,
        context: summary, // Pass summary for context-aware answers
      });

      const botMsg = { sender: "bot", text: res.data.response };
      setChatMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      console.error(err);
      setChatMessages((prev) => [
        ...prev,
        { sender: "bot", text: "Sorry, I ran into an issue answering that." },
      ]);
    } finally {
      setChatLoading(false);
    }
  };

  return (
    <div className="app">
      <h1>🎬 YouTube AI Summarizer & Chat Assistant</h1>

      {/* YouTube URL Input */}
      <div className="input-group">
        <input
          type="text"
          placeholder="Paste YouTube video URL..."
          value={youtubeURL}
          onChange={(e) => setYoutubeURL(e.target.value)}
        />
        <button onClick={handleSummarize} disabled={loading}>
          {loading ? "Summarizing..." : "Summarize Video"}
        </button>
      </div>

      {/* Error Message */}
      {errorMessage && (
        <div className="error-card">
          <p>⚠️ {errorMessage}</p>
        </div>
      )}

      {/* Summary Output */}
      {summary && (
        <div className="summary">
          <h2>📝 Video Summary</h2>
          <ReactMarkdown>{summary}</ReactMarkdown>
        </div>
      )}

      <hr style={{ margin: "30px 0" }} />

      {/* AI Chatbot */}
      <div className="chat-section">
        <h2>💬 Chat Assistant</h2>
        <div className="chat-box">
          {chatMessages.map((msg, idx) => (
            <div key={idx} className={`chat-message ${msg.sender}`}>
              <strong>{msg.sender === "user" ? "You: " : "AI: "}</strong>
              <ReactMarkdown>{msg.text}</ReactMarkdown>
            </div>
          ))}
          {chatLoading && <p className="chat-loading">AI is typing...</p>}
        </div>

        <div className="chat-input-container">
          <input
            type="text"
            placeholder="Ask a question about the video summary..."
            value={chatInput}
            onChange={(e) => setChatInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSendMessage()}
          />
          <button onClick={handleSendMessage} disabled={chatLoading}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;