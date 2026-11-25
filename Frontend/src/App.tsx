import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import { useState, useEffect } from 'react'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Submissions from './pages/Submissions'
import Investigations from './pages/Investigations'
import InvestigationDetail from './pages/InvestigationDetail'
import Reports from './pages/Reports'
import Students from './pages/Students'
import MCPTools from './pages/MCPTools'
import Settings from './pages/Settings'
import AuditLog from './pages/AuditLog'
import Login from './pages/Login'

function App() {
  const [isDarkMode, setIsDarkMode] = useState(false)
  const [isAuthenticated, setIsAuthenticated] = useState(!!localStorage.getItem('token'))

  useEffect(() => {
    const savedTheme = localStorage.getItem('theme')
    if (savedTheme === 'dark') {
      setIsDarkMode(true)
      document.documentElement.classList.add('dark')
    }
  }, [])

  const toggleTheme = () => {
    const newDarkMode = !isDarkMode
    setIsDarkMode(newDarkMode)
    
    if (newDarkMode) {
      document.documentElement.classList.add('dark')
      localStorage.setItem('theme', 'dark')
    } else {
      document.documentElement.classList.remove('dark')
      localStorage.setItem('theme', 'light')
    }
  }

  if (!isAuthenticated) {
    return (
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<Login setIsAuthenticated={setIsAuthenticated} />} />
          <Route path="*" element={<Navigate to="/login" replace />} />
        </Routes>
      </BrowserRouter>
    )
  }

  return (
    <BrowserRouter>
      <Layout isDarkMode={isDarkMode} toggleTheme={toggleTheme} onLogout={() => setIsAuthenticated(false)}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/submissions" element={<Submissions />} />
          <Route path="/investigations" element={<Investigations />} />
          <Route path="/investigations/:id" element={<InvestigationDetail />} />
          <Route path="/reports" element={<Reports />} />
          <Route path="/students" element={<Students />} />
          <Route path="/mcp-tools" element={<MCPTools />} />
          <Route path="/settings" element={<Settings />} />
          <Route path="/audit-log" element={<AuditLog />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </Layout>
    </BrowserRouter>
  )
}

export default App
