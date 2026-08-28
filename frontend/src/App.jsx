import { useState } from 'react'
import './App.css'

const API_URL = 'http://127.0.0.1:8000/ask'

function App() {
  const [question, setQuestion]=useState("");
  const [answer, setAnswer]=useState(null);
  const [loading, setLoading]=useState(false);
  

  const handleAsk = async () => {
    setLoading(true);
    setAnswer(null);
    try {
      const response = await fetch(API_URL, {
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

export default App
