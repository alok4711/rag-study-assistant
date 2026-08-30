import { useState } from 'react'
import './AskPage.css'

const API_URL = import.meta.env.VITE_API_URL

function AskPage() {
  const [question, setQuestion]=useState("");
  const [answer, setAnswer]=useState(null);
  const [loading, setLoading]=useState(false);
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState("");


  const handleUpload = async () => {
    if (!selectedFile) {
      setUploadStatus("Please select a file to upload.");
      return;
    }

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(`${API_URL}/upload`, {
        method: "POST",
        body: formData
      });

      const data = await response.json();

      if(!response.ok) {
        throw new Error(data.detail || "File upload failed.");
      }

      setUploadStatus("File uploaded successfully.");
    }
    catch (error) {
      setUploadStatus(`Error: ${error.message}`);
    }
  };
  

  const handleAsk = async () => {
    setLoading(true);
    setAnswer(null);
    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: 'POST',
        headers:{
          "Content-Type": "application/json"
        },
        body: JSON.stringify({ 
          question : question
        })
      });

      const data = await response.json();
      setAnswer(data);
    }
    catch (error) {
      setAnswer({ 
        answer: "Something went wrong.", 
        sources: [] 
      });
    }
    finally {
      setLoading(false);
    }
  };


  return (
    <div className="app">
      <h1>RAG Study Assistant</h1>
      <p className="subtitle">Ask a question about your notes</p>

      {/* File Upload */}
      <div className="upload-box">
        <input
          type="file"
          accept=".txt"
          onChange={(e) => setSelectedFile(e.target.files[0])}
        />

        <button
          type="button"
          onClick={handleUpload}
        >
          Upload
        </button>

        {uploadStatus && <p>{uploadStatus}</p>}
      </div>

      {/* Ask Question */}
      <div className="ask-box">
        <input
          type="text"
          placeholder="e.g. What is the time complexity of quicksort?"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
        />

        <button 
          type="button" 
          onClick={handleAsk}
          disabled={loading}
        >
          Ask
        </button>
      </div>

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
