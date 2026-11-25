import { useEffect, useState } from 'react'
import { mcpAPI } from '../services/api'

export default function MCPTools() {
  const [mcpStatus, setMcpStatus] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchMCPStatus()
  }, [])

  const fetchMCPStatus = async () => {
    try {
      const response = await mcpAPI.getStatus()
      setMcpStatus(response.data)
    } catch (error) {
      console.error('Failed to fetch MCP status:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-[#0F172A] dark:text-[#F8FAFC]">MCP Tools</h1>
        <p className="text-[#64748B] dark:text-[#94A3B8] mt-2">
          Model Context Protocol server status and tools
        </p>
      </div>

      {loading ? (
        <div className="text-center py-12 text-[#64748B]">Loading...</div>
      ) : mcpStatus ? (
        <div className="space-y-4">
          <div className="bg-white dark:bg-[#172033] rounded-lg border border-[#E2E8F0] dark:border-[#293548] p-6">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm text-[#64748B] dark:text-[#94A3B8]">Mode</p>
                <p className="text-2xl font-bold text-[#0F172A] dark:text-[#F8FAFC]">
                  {mcpStatus.mode}
                </p>
              </div>
              <div className="text-4xl">{mcpStatus.mode === 'mock' ? '🔄' : '✓'}</div>
            </div>
          </div>

          {mcpStatus.servers?.map((server: any, idx: number) => (
            <div
              key={idx}
              className="bg-white dark:bg-[#172033] rounded-lg border border-[#E2E8F0] dark:border-[#293548] p-6"
            >
              <h3 className="text-lg font-bold text-[#0F172A] dark:text-[#F8FAFC] mb-4">
                {server.name}
              </h3>
              <div className="mb-4">
                <span
                  className={`text-xs font-medium px-2 py-1 rounded ${
                    server.connected
                      ? 'bg-green-100 dark:bg-green-900/20 text-green-700 dark:text-green-400'
                      : 'bg-red-100 dark:bg-red-900/20 text-red-700 dark:text-red-400'
                  }`}
                >
                  {server.connected ? 'Connected' : 'Disconnected'}
                </span>
              </div>
              <div>
                <p className="text-sm font-medium text-[#0F172A] dark:text-[#F8FAFC] mb-2">
                  Available Tools:
                </p>
                <div className="space-y-2">
                  {server.tools?.map((tool: any, tidx: number) => (
                    <div
                      key={tidx}
                      className="p-3 bg-[#F8FAFC] dark:bg-[#111827] rounded border border-[#E2E8F0] dark:border-[#293548]"
                    >
                      <p className="text-sm font-mono text-[#0F172A] dark:text-[#F8FAFC]">
                        {tool.name}
                      </p>
                      <p className="text-xs text-[#64748B] dark:text-[#94A3B8]">
                        {tool.description}
                      </p>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12 text-[#64748B]">Failed to load MCP status</div>
      )}
    </div>
  )
}
