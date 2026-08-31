import { useState, useRef } from 'react'
import './AskPage.css'

const API_URL = import.meta.env.VITE_API_URL

function AskPage() {
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [loading, setLoading] = useState(false);
  const [uploadStatus, setUploadStatus] = useState("");
  const [listening, setListening] = useState(false);
  const fileInputRef = useRef(null);

  const handleFileSelected = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploadStatus(`Uploading ${file.name}...`);
    try {
      const formData = new FormData();
      formData.append("file", file);

      const response = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "File upload failed.");

      setUploadStatus(`Indexed ${file.name} (${data.chunks_indexed} chunks)`);
    } catch (error) {
      setUploadStatus(`Error: ${error.message}`);
    } finally {
      e.target.value = "";
    }
  };

  const handleVoiceInput = () => {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      setUploadStatus("Voice input isn't supported in this browser.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.interimResults = false;

    recognition.onstart = () => setListening(true);
    recognition.onend = () => setListening(false);
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setQuestion((prev) => (prev ? prev + " " + transcript : transcript));
    };

    recognition.start();
  };

  const handleAsk = async () => {
    if (!question.trim()) return;
    setLoading(true);
    setAnswer(null);
    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: 'POST',
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ question })
      });
      const data = await response.json();
      setAnswer(data);
    } catch (error) {
      setAnswer({ answer: "Something went wrong.", sources: [] });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="app">
      <h1>RAG Study Assistant</h1>
      <p className="subtitle">Ask a question about your notes</p>

      <div className="ask-box">
        <input
          type="file"
          accept=".txt"
          ref={fileInputRef}
          onChange={handleFileSelected}
          style={{ display: "none" }}
        />
        <button
          type="button"
          className="attach-btn"
          onClick={() => fileInputRef.current.click()}
          title="Upload a note"
        >
          +
        </button>

        <input
          type="text"
          placeholder="e.g. What is the time complexity of quicksort?"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && handleAsk()}
        />

        <button
          type="button"
          className={`mic-btn ${listening ? "listening" : ""}`}
          onClick={handleVoiceInput}
          title="Ask with your voice"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="currentColor">
            <path d="M12 15a3 3 0 0 0 3-3V6a3 3 0 0 0-6 0v6a3 3 0 0 0 3 3z"/>
            <path d="M19 11a1 1 0 0 0-2 0 5 5 0 0 1-10 0 1 1 0 0 0-2 0 7 7 0 0 0 6 6.92V20H8a1 1 0 0 0 0 2h8a1 1 0 0 0 0-2h-3v-2.08A7 7 0 0 0 19 11z"/>
          </svg>
        </button>

        {question.trim() && (
          <button
            type="button"
            className="send-btn"
            onClick={handleAsk}
            disabled={loading}
            title="Send"
          >
            <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
              <path d="M2 21l21-9L2 3v7l15 2-15 2z"/>
            </svg>
          </button>
        )}
      </div>

      {uploadStatus && <p className="upload-status">{uploadStatus}</p>}
      {loading && <p className="loading">Thinking...</p>}

      {answer && (
        <div className="answer-box">
          <p className="answer-text">{answer.answer}</p>
          <div className="sources">
            Sources: {answer.sources.map((s, i) => <span key={i}>{s}</span>)}
          </div>
        </div>
      )}
    </div>
  )
}

export default AskPage