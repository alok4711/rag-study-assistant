import { BrowserRouter, Routes, Route, Link } from 'react-router-dom'
import AskPage from './pages/AskPage'
import EvaluatePage from './pages/EvaluatePage'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <nav className="navbar">
        <Link to="/">Ask</Link>
        <Link to="/evaluate">Evaluation Dashboard</Link>
      </nav>

      <Routes>
        <Route path="/" element={<AskPage />} />
        <Route path="/evaluate" element={<EvaluatePage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App