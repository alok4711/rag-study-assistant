import { useState, useRef } from "react";
import "./EvaluatePage.css";

const API_URL = import.meta.env.VITE_API_URL;

function EvaluatePage() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const fileInputRef = useRef(null);

  const handleEvaluate = async () => {
    if (!selectedFile) {
      setError("Please select a CSV file.");
      return;
    }

    setLoading(true);
    setError("");
    setResults(null);

    try {
      const formData = new FormData();
      formData.append("file", selectedFile);

      const response = await fetch(`${API_URL}/evaluate`, {
        method: "POST",
        body: formData
      });

      const data = await response.json();
      if (!response.ok) throw new Error(data.detail || "Evaluation failed.");

      setResults(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="evaluate-page">
      <h1>Evaluation Dashboard</h1>
      <p className="subtitle">Upload a CSV test set to evaluate your RAG system.</p>

      <div className="upload-box">
        <input
          type="file"
          accept=".csv"
          ref={fileInputRef}
          onChange={(e) => setSelectedFile(e.target.files[0])}
          style={{ display: "none" }}
        />

        <button
          type="button"
          className="choose-file-btn"
          onClick={() => fileInputRef.current.click()}
        >
          Choose CSV
        </button>

        <span className="file-name">
          {selectedFile ? selectedFile.name : "No file chosen"}
        </span>

        <button
          type="button"
          className="run-btn"
          onClick={handleEvaluate}
          disabled={loading || !selectedFile}
        >
          {loading ? "Evaluating..." : "Run Evaluation"}
        </button>
      </div>

      {error && <p className="error">{error}</p>}

      {results && (
        <div className="evaluation-results">
          <h2>Summary</h2>
          <p>
            Average Score: <strong>{results.average_score}</strong>
            {" | "}
            Total Questions: <strong>{results.total_questions}</strong>
          </p>

          <table>
            <thead>
              <tr>
                <th>Question</th>
                <th>Score</th>
                <th>Reasoning</th>
              </tr>
            </thead>
            <tbody>
              {results.results.map((item, index) => (
                <tr key={index}>
                  <td>{item.question}</td>
                  <td>
                    <span className={`score-badge score-${item.score}`}>{item.score}/5</span>
                  </td>
                  <td>{item.reasoning}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export default EvaluatePage;