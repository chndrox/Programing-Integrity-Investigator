import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import axios from 'axios'

interface LoginProps {
  setIsAuthenticated: (value: boolean) => void
}

export default function Login({ setIsAuthenticated }: LoginProps) {
  const navigate = useNavigate()
  const [username, setUsername] = useState('instructor1')
  const [password, setPassword] = useState('password123')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setError('')
    setLoading(true)

    try {
      const response = await axios.post('http://localhost:8000/api/auth/login', {
        username,
        password,
      }, {
        headers: {
          'Content-Type': 'application/json',
        },
      })

      localStorage.setItem('token', response.data.access_token)
      localStorage.setItem('user', JSON.stringify(response.data.user))
      setIsAuthenticated(true)
      navigate('/')
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Login failed. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-[#F8FAFC] dark:bg-[#0B1120] flex items-center justify-center">
      <div className="w-full max-w-md">
        <div className="bg-white dark:bg-[#172033] rounded-lg shadow-lg p-8">
          {/* Logo */}
          <div className="text-center mb-8">
            <div className="text-5xl mb-4">🔬</div>
            <h1 className="text-3xl font-bold text-[#0F172A] dark:text-[#F8FAFC]">
              Programming Assignment
            </h1>
            <p className="text-lg text-[#4F46E5] dark:text-[#818CF8] font-semibold">
              Integrity Investigator
            </p>
          </div>

          {/* Login Form */}
          <form onSubmit={handleLogin}>
            <div className="mb-4">
              <label className="block text-sm font-medium text-[#0F172A] dark:text-[#F8FAFC] mb-2">
                Username
              </label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                className="w-full px-4 py-2 border border-[#E2E8F0] dark:border-[#293548] rounded-lg bg-white dark:bg-[#111827] text-[#0F172A] dark:text-[#F8FAFC] focus:outline-none focus:ring-2 focus:ring-[#4F46E5] dark:focus:ring-[#818CF8]"
                disabled={loading}
              />
            </div>

            <div className="mb-6">
              <label className="block text-sm font-medium text-[#0F172A] dark:text-[#F8FAFC] mb-2">
                Password
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2 border border-[#E2E8F0] dark:border-[#293548] rounded-lg bg-white dark:bg-[#111827] text-[#0F172A] dark:text-[#F8FAFC] focus:outline-none focus:ring-2 focus:ring-[#4F46E5] dark:focus:ring-[#818CF8]"
                disabled={loading}
              />
            </div>

            {error && (
              <div className="mb-4 p-3 bg-red-100 dark:bg-red-900/20 border border-red-300 dark:border-red-800 text-red-700 dark:text-red-400 rounded-lg text-sm">
                {error}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-[#4F46E5] dark:bg-[#818CF8] text-white py-2 rounded-lg font-medium hover:bg-[#4338CA] dark:hover:bg-[#6366F1] transition-colors disabled:opacity-50"
            >
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </form>

          {/* Demo Info */}
          <div className="mt-6 p-4 bg-[#F8FAFC] dark:bg-[#111827] rounded-lg border border-[#E2E8F0] dark:border-[#293548]">
            <p className="text-xs text-[#64748B] dark:text-[#94A3B8] mb-2">
              Demo credentials:
            </p>
            <p className="text-xs text-[#0F172A] dark:text-[#F8FAFC] font-mono">
              Username: instructor1
            </p>
            <p className="text-xs text-[#0F172A] dark:text-[#F8FAFC] font-mono">
              Password: password123
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
