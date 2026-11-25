import { useEffect, useState } from 'react'
import { auditAPI } from '../services/api'

export default function AuditLog() {
  const [logs, setLogs] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchLogs()
  }, [])

  const fetchLogs = async () => {
    try {
      const response = await auditAPI.getLogs(100)
      setLogs(response.data)
    } catch (error) {
      console.error('Failed to fetch audit logs:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-[#0F172A] dark:text-[#F8FAFC]">Audit Log</h1>
        <p className="text-[#64748B] dark:text-[#94A3B8] mt-2">
          Track all system activities and investigations
        </p>
      </div>

      <div className="bg-white dark:bg-[#172033] rounded-lg border border-[#E2E8F0] dark:border-[#293548] overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-[#F8FAFC] dark:bg-[#111827] border-b border-[#E2E8F0] dark:border-[#293548]">
              <tr>
                <th className="px-6 py-3 text-left text-sm font-semibold text-[#0F172A] dark:text-[#F8FAFC]">
                  User
                </th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-[#0F172A] dark:text-[#F8FAFC]">
                  Action
                </th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-[#0F172A] dark:text-[#F8FAFC]">
                  Details
                </th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-[#0F172A] dark:text-[#F8FAFC]">
                  Timestamp
                </th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={4} className="px-6 py-4 text-center text-[#64748B]">
                    Loading...
                  </td>
                </tr>
              ) : logs.length === 0 ? (
                <tr>
                  <td colSpan={4} className="px-6 py-4 text-center text-[#64748B]">
                    No audit logs yet
                  </td>
                </tr>
              ) : (
                logs.map((log, idx) => (
                  <tr
                    key={idx}
                    className="border-b border-[#E2E8F0] dark:border-[#293548] hover:bg-[#F8FAFC] dark:hover:bg-[#111827]"
                  >
                    <td className="px-6 py-4 text-sm text-[#0F172A] dark:text-[#F8FAFC]">
                      {log.user}
                    </td>
                    <td className="px-6 py-4 text-sm text-[#0F172A] dark:text-[#F8FAFC] font-mono">
                      {log.action}
                    </td>
                    <td className="px-6 py-4 text-sm text-[#64748B] dark:text-[#94A3B8]">
                      {log.details ? JSON.stringify(log.details).substring(0, 50) + '...' : '-'}
                    </td>
                    <td className="px-6 py-4 text-sm text-[#64748B] dark:text-[#94A3B8]">
                      {new Date(log.created_at).toLocaleString()}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  )
}
