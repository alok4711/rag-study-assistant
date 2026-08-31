import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom'
import AskPage from './pages/AskPage'
import EvaluatePage from './pages/EvaluatePage'
import './App.css'

function App() {
  return (
    <BrowserRouter>
      <nav className="navbar">
        <NavLink to="/">Ask</NavLink>
        <NavLink to="/evaluate">Evaluation Dashboard</NavLink>
      </nav>

      <Routes>
        <Route path="/" element={<AskPage />} />
        <Route path="/evaluate" element={<EvaluatePage />} />
      </Routes>
    </BrowserRouter>
  )
}

export default App