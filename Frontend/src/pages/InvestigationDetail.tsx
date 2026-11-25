import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { investigationsAPI } from '../services/api'

export default function InvestigationDetail() {
  const { id } = useParams<{ id: string }>()
  const [investigation, setInvestigation] = useState<any>(null)
  const [report, setReport] = useState<any>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchInvestigation()
  }, [id])

  const fetchInvestigation = async () => {
    try {
      const response = await investigationsAPI.get(Number(id))
      setInvestigation(response.data)

      if (response.data.status === 'completed') {
        try {
          const reportRes = await investigationsAPI.getReport(Number(id))
          setReport(reportRes.data)
        } catch (error) {
          console.error('Failed to fetch report:', error)
        }
      }
    } catch (error) {
      console.error('Failed to fetch investigation:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-xl text-[#64748B]">Loading investigation...</div>
      </div>
    )
  }

  if (!investigation) {
    return (
      <div className="text-center py-12">
        <p className="text-[#64748B]">Investigation not found</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-[#0F172A] dark:text-[#F8FAFC]">
          Investigation #{investigation.id}
        </h1>
        <p className="text-[#64748B] dark:text-[#94A3B8] mt-2">
          {investigation.assignment_name}
        </p>
      </div>

      {/* Investigation Status */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white dark:bg-[#172033] p-4 rounded-lg border border-[#E2E8F0] dark:border-[#293548]">
          <p className="text-sm text-[#64748B] dark:text-[#94A3B8]">Status</p>
          <p className="text-2xl font-bold text-[#0F172A] dark:text-[#F8FAFC]">{investigation.status}</p>
        </div>
        <div className="bg-white dark:bg-[#172033] p-4 rounded-lg border border-[#E2E8F0] dark:border-[#293548]">
          <p className="text-sm text-[#64748B] dark:text-[#94A3B8]">Submissions</p>
          <p className="text-2xl font-bold text-[#0F172A] dark:text-[#F8FAFC]">{investigation.submission_count}</p>
        </div>
        <div className="bg-white dark:bg-[#172033] p-4 rounded-lg border border-[#E2E8F0] dark:border-[#293548]">
          <p className="text-sm text-[#64748B] dark:text-[#94A3B8]">Created</p>
          <p className="text-sm font-mono text-[#0F172A] dark:text-[#F8FAFC]">
            {new Date(investigation.created_at).toLocaleDateString()}
          </p>
        </div>
        <div className="bg-white dark:bg-[#172033] p-4 rounded-lg border border-[#E2E8F0] dark:border-[#293548]">
          <p className="text-sm text-[#64748B] dark:text-[#94A3B8]">Has Report</p>
          <p className="text-2xl font-bold">{investigation.report ? '✓' : '✗'}</p>
        </div>
      </div>

      {/* Submitted Submissions */}
      <div className="bg-white dark:bg-[#172033] rounded-lg border border-[#E2E8F0] dark:border-[#293548] p-6">
        <h2 className="text-lg font-bold text-[#0F172A] dark:text-[#F8FAFC] mb-4">
          Submissions Under Investigation
        </h2>
        <div className="space-y-3">
          {investigation.submissions.map((sub: any) => (
            <div
              key={sub.id}
              className="p-4 bg-[#F8FAFC] dark:bg-[#111827] rounded-lg border border-[#E2E8F0] dark:border-[#293548]"
            >
              <p className="font-medium text-[#0F172A] dark:text-[#F8FAFC]">{sub.student_name}</p>
              <p className="text-sm text-[#64748B] dark:text-[#94A3B8]">
                {new Date(sub.submitted_at).toLocaleString()}
              </p>
            </div>
          ))}
        </div>
      </div>

      {/* Agent Results */}
      {investigation.agent_results && investigation.agent_results.length > 0 && (
        <div className="bg-white dark:bg-[#172033] rounded-lg border border-[#E2E8F0] dark:border-[#293548] p-6">
          <h2 className="text-lg font-bold text-[#0F172A] dark:text-[#F8FAFC] mb-4">
            Agent Analysis Results
          </h2>
          <div className="space-y-4">
            {investigation.agent_results.map((result: any, idx: number) => (
              <div
                key={idx}
                className="p-4 bg-[#F8FAFC] dark:bg-[#111827] rounded-lg border border-[#E2E8F0] dark:border-[#293548]"
              >
                <div className="flex items-center justify-between">
                  <div>
                    <p className="font-medium text-[#0F172A] dark:text-[#F8FAFC]">
                      {result.agent_type.replace(/_/g, ' ').toUpperCase()}
                    </p>
                    <p className="text-sm text-[#64748B] dark:text-[#94A3B8]">
                      Status: {result.status} | Execution: {result.execution_time?.toFixed(2)}s
                    </p>
                  </div>
                  <span
                    className={`text-xs font-medium px-2 py-1 rounded ${
                      result.status === 'completed'
                        ? 'bg-green-100 dark:bg-green-900/20 text-green-700 dark:text-green-400'
                        : 'bg-red-100 dark:bg-red-900/20 text-red-700 dark:text-red-400'
                    }`}
                  >
                    {result.status}
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Report */}
      {report && (
        <div className="bg-white dark:bg-[#172033] rounded-lg border border-[#E2E8F0] dark:border-[#293548] p-6">
          <h2 className="text-lg font-bold text-[#0F172A] dark:text-[#F8FAFC] mb-4">
            Investigation Report
          </h2>
          <div className="text-sm text-[#0F172A] dark:text-[#F8FAFC] whitespace-pre-wrap">
            {JSON.stringify(report, null, 2)}
          </div>
        </div>
      )}
    </div>
  )
}
