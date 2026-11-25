import { ReactNode, useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Menu, X, Moon, Sun, LogOut } from 'lucide-react'

interface LayoutProps {
  children: ReactNode
  isDarkMode: boolean
  toggleTheme: () => void
  onLogout: () => void
}

export default function Layout({ children, isDarkMode, toggleTheme, onLogout }: LayoutProps) {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true)
  const location = useLocation()

  const navigationItems = [
    { label: 'Dashboard', path: '/', icon: '📊' },
    { label: 'Submissions', path: '/submissions', icon: '📤' },
    { label: 'Investigations', path: '/investigations', icon: '🔍' },
    { label: 'Reports', path: '/reports', icon: '📋' },
    { label: 'Students', path: '/students', icon: '👥' },
    { label: 'MCP Tools', path: '/mcp-tools', icon: '🔧' },
    { label: 'Audit Log', path: '/audit-log', icon: '📝' },
    { label: 'Settings', path: '/settings', icon: '⚙️' },
  ]

  const isActive = (path: string) => location.pathname === path

  const handleLogout = () => {
    localStorage.removeItem('token')
    onLogout()
  }

  return (
    <div className={`flex h-screen ${isDarkMode ? 'dark' : ''}`}>
      {/* Sidebar */}
      <div className={`${
        isDarkMode
          ? 'bg-[#111827] border-[#293548]'
          : 'bg-white border-[#E2E8F0]'
      } border-r transition-all duration-300 ${isSidebarOpen ? 'w-64' : 'w-20'}`}>
        <div className="flex flex-col h-full">
          {/* Logo */}
          <div className={`flex items-center justify-center h-16 ${
            isDarkMode ? 'border-[#293548]' : 'border-[#E2E8F0]'
          } border-b`}>
            <span className={`text-2xl font-bold ${isDarkMode ? 'text-[#818CF8]' : 'text-[#4F46E5]'}`}>
              {isSidebarOpen ? '🔬 PII' : '🔬'}
            </span>
          </div>

          {/* Navigation */}
          <nav className="flex-1 overflow-y-auto py-4">
            {navigationItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center px-4 py-3 mx-2 rounded-lg transition-colors ${
                  isActive(item.path)
                    ? isDarkMode
                      ? 'bg-[#818CF8] text-white'
                      : 'bg-[#4F46E5] text-white'
                    : isDarkMode
                    ? 'text-[#F8FAFC] hover:bg-[#293548]'
                    : 'text-[#0F172A] hover:bg-[#F8FAFC]'
                }`}
              >
                <span className="text-xl">{item.icon}</span>
                {isSidebarOpen && <span className="ml-3">{item.label}</span>}
              </Link>
            ))}
          </nav>

          {/* Footer */}
          <div className={`${
            isDarkMode ? 'border-[#293548]' : 'border-[#E2E8F0]'
          } border-t p-4`}>
            <button
              onClick={handleLogout}
              className={`w-full flex items-center justify-center py-2 px-3 rounded-lg transition-colors ${
                isDarkMode
                  ? 'bg-red-900/20 text-red-400 hover:bg-red-900/30'
                  : 'bg-red-100 text-red-700 hover:bg-red-200'
              }`}
            >
              <LogOut size={18} />
              {isSidebarOpen && <span className="ml-2">Logout</span>}
            </button>
          </div>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top Bar */}
        <div className={`${
          isDarkMode
            ? 'bg-[#111827] border-[#293548]'
            : 'bg-white border-[#E2E8F0]'
        } border-b px-6 py-4 flex items-center justify-between`}>
          <button
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className={`p-2 rounded-lg ${
              isDarkMode ? 'hover:bg-[#293548]' : 'hover:bg-[#F8FAFC]'
            }`}
          >
            {isSidebarOpen ? <X size={20} /> : <Menu size={20} />}
          </button>

          <div className="flex items-center gap-4">
            <button
              onClick={toggleTheme}
              className={`p-2 rounded-lg transition-colors ${
                isDarkMode
                  ? 'bg-[#293548] text-[#818CF8] hover:bg-[#3A4557]'
                  : 'bg-[#F8FAFC] text-[#4F46E5] hover:bg-[#E2E8F0]'
              }`}
            >
              {isDarkMode ? <Sun size={20} /> : <Moon size={20} />}
            </button>
          </div>
        </div>

        {/* Page Content */}
        <main className={`flex-1 overflow-auto ${
          isDarkMode ? 'bg-[#0B1120]' : 'bg-[#F8FAFC]'
        }`}>
          <div className="p-6">
            {children}
          </div>
        </main>
      </div>
    </div>
  )
}
