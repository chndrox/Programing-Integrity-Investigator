import { useEffect, useState } from 'react'
import { settingsAPI } from '../services/api'

export default function Settings() {
  const [settings, setSettings] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchSettings()
  }, [])

  const fetchSettings = async () => {
    try {
      const response = await settingsAPI.get()
      setSettings(response.data)
    } catch (error) {
      console.error('Failed to fetch settings:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-[#0F172A] dark:text-[#F8FAFC]">Settings</h1>
        <p className="text-[#64748B] dark:text-[#94A3B8] mt-2">
          Configure application settings and preferences
        </p>
      </div>

      {loading ? (
        <div className="text-center py-12 text-[#64748B]">Loading settings...</div>
      ) : settings ? (
        <div className="bg-white dark:bg-[#172033] rounded-lg border border-[#E2E8F0] dark:border-[#293548] p-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <label className="block text-sm font-medium text-[#0F172A] dark:text-[#F8FAFC] mb-2">
                Groq Model
              </label>
              <div className="p-3 bg-[#F8FAFC] dark:bg-[#111827] rounded border border-[#E2E8F0] dark:border-[#293548] text-[#0F172A] dark:text-[#F8FAFC]">
                {settings.groq_model}
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-[#0F172A] dark:text-[#F8FAFC] mb-2">
                Agent Concurrency Limit
              </label>
              <div className="p-3 bg-[#F8FAFC] dark:bg-[#111827] rounded border border-[#E2E8F0] dark:border-[#293548] text-[#0F172A] dark:text-[#F8FAFC]">
                {settings.agent_concurrency_limit}
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-[#0F172A] dark:text-[#F8FAFC] mb-2">
                Agent Timeout (seconds)
              </label>
              <div className="p-3 bg-[#F8FAFC] dark:bg-[#111827] rounded border border-[#E2E8F0] dark:border-[#293548] text-[#0F172A] dark:text-[#F8FAFC]">
                {settings.agent_timeout_seconds}
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-[#0F172A] dark:text-[#F8FAFC] mb-2">
                MCP Mode
              </label>
              <div className="p-3 bg-[#F8FAFC] dark:bg-[#111827] rounded border border-[#E2E8F0] dark:border-[#293548] text-[#0F172A] dark:text-[#F8FAFC]">
                {settings.use_mock_mcp ? 'Mock' : 'Live'}
              </div>
            </div>
          </div>
        </div>
      ) : (
        <div className="text-center py-12 text-[#64748B]">Failed to load settings</div>
      )}
    </div>
  )
}
