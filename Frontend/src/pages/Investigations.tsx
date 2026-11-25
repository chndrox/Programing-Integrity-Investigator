import { useEffect, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { investigationsAPI, submissionsAPI } from '../services/api'

export default function Investigations() {
  const navigate = useNavigate()
  const [investigations, setInvestigations] = useState<any[]>([])
  const [submissions, setSubmissions] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [showNewInvestigation, setShowNewInvestigation] = useState(false)
  const [selectedSubmissions, setSelectedSubmissions] = useState<number[]>([])
  const [assignmentId, setAssignmentId] = useState<number>(1)
  const [startingInvestigation, setStartingInvestigation] = useState(false)

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    try {
      const [investRes, submissionsRes] = await Promise.all([
        investigationsAPI.list(),
        submissionsAPI.list(),
      ])
      setInvestigations(investRes.data)
      setSubmissions(submissionsRes.data)
    } catch (error) {
      console.error('Failed to fetch data:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleStartInvestigation = async () => {
    if (selectedSubmissions.length < 2) {
      alert('Select at least 2 submissions')
      return
    }

    setStartingInvestigation(true)
    try {
      const response = await investigationsAPI.start({
        assignment_id: assignmentId,
        submission_ids: selectedSubmissions,
      })
      alert('Investigation started!')
      setShowNewInvestigation(false)
      setSelectedSubmissions([])
      fetchData()
    } catch (error) {
      alert('Failed to start investigation')
      console.error(error)
    } finally {
      setStartingInvestigation(false)
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-[#0F172A] dark:text-[#F8FAFC]">
            Investigations
          </h1>
          <p className="text-[#64748B] dark:text-[#94A3B8] mt-2">
            Monitor plagiarism investigations
          </p>
        </div>
        <button
          onClick={() => setShowNewInvestigation(!showNewInvestigation)}
          className="bg-[#4F46E5] dark:bg-[#818CF8] text-white px-4 py-2 rounded-lg font-medium hover:bg-[#4338CA]"
        >
          + New Investigation
        </button>
      </div>

      {/* New Investigation Form */}
      {showNewInvestigation && (
        <div className="bg-white dark:bg-[#172033] rounded-lg border border-[#E2E8F0] dark:border-[#293548] p-6">
          <h2 className="text-lg font-bold text-[#0F172A] dark:text-[#F8FAFC] mb-4">
            Start New Investigation
          </h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-[#0F172A] dark:text-[#F8FAFC] mb-2">
                Assignment ID
              </label>
              <input
                type="number"
                value={assignmentId}
                onChange={(e) => setAssignmentId(Number(e.target.value))}
                className="w-full px-4 py-2 border border-[#E2E8F0] dark:border-[#293548] rounded-lg bg-white dark:bg-[#111827]"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-[#0F172A] dark:text-[#F8FAFC] mb-2">
                Select Submissions (at least 2)
              </label>
              <div className="space-y-2 max-h-64 overflow-y-auto">
                {submissions.map((submission) => (
                  <label
                    key={submission.id}
                    className="flex items-center p-2 hover:bg-[#F8FAFC] dark:hover:bg-[#111827] rounded cursor-pointer"
                  >
                    <input
                      type="checkbox"
                      checked={selectedSubmissions.includes(submission.id)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setSelectedSubmissions([...selectedSubmissions, submission.id])
                        } else {
                          setSelectedSubmissions(
                            selectedSubmissions.filter((id) => id !== submission.id)
                          )
                        }
                      }}
                      className="mr-3"
                    />
                    <span className="text-sm text-[#0F172A] dark:text-[#F8FAFC]">
                      {submission.student_name} - {submission.file_name}
                    </span>
                  </label>
                ))}
              </div>
            </div>
            <div className="flex gap-3">
              <button
                onClick={handleStartInvestigation}
                disabled={startingInvestigation || selectedSubmissions.length < 2}
                className="flex-1 bg-[#4F46E5] dark:bg-[#818CF8] text-white py-2 rounded-lg font-medium hover:bg-[#4338CA] disabled:opacity-50"
              >
                {startingInvestigation ? 'Starting...' : 'Start Investigation'}
              </button>
              <button
                onClick={() => setShowNewInvestigation(false)}
                className="flex-1 bg-[#E2E8F0] dark:bg-[#293548] text-[#0F172A] dark:text-[#F8FAFC] py-2 rounded-lg font-medium hover:bg-[#CBD5E1]"
              >
                Cancel
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Investigations List */}
      <div className="bg-white dark:bg-[#172033] rounded-lg border border-[#E2E8F0] dark:border-[#293548] overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-[#F8FAFC] dark:bg-[#111827] border-b border-[#E2E8F0] dark:border-[#293548]">
              <tr>
                <th className="px-6 py-3 text-left text-sm font-semibold text-[#0F172A] dark:text-[#F8FAFC]">
                  ID
                </th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-[#0F172A] dark:text-[#F8FAFC]">
                  Assignment
                </th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-[#0F172A] dark:text-[#F8FAFC]">
                  Submissions
                </th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-[#0F172A] dark:text-[#F8FAFC]">
                  Status
                </th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-[#0F172A] dark:text-[#F8FAFC]">
                  Created
                </th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-[#0F172A] dark:text-[#F8FAFC]">
                  Action
                </th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={6} className="px-6 py-4 text-center text-[#64748B]">
                    Loading...
                  </td>
                </tr>
              ) : investigations.length === 0 ? (
                <tr>
                  <td colSpan={6} className="px-6 py-4 text-center text-[#64748B]">
                    No investigations yet
                  </td>
                </tr>
              ) : (
                investigations.map((inv) => (
                  <tr
                    key={inv.id}
                    className="border-b border-[#E2E8F0] dark:border-[#293548] hover:bg-[#F8FAFC] dark:hover:bg-[#111827]"
                  >
                    <td className="px-6 py-4 text-sm text-[#0F172A] dark:text-[#F8FAFC] font-mono">
                      #{inv.id}
                    </td>
                    <td className="px-6 py-4 text-sm text-[#0F172A] dark:text-[#F8FAFC]">
                      {inv.assignment_name}
                    </td>
                    <td className="px-6 py-4 text-sm text-[#64748B] dark:text-[#94A3B8]">
                      {inv.submission_count}
                    </td>
                    <td className="px-6 py-4">
                      <span
                        className={`text-xs font-medium px-2 py-1 rounded ${
                          inv.status === 'completed'
                            ? 'bg-green-100 dark:bg-green-900/20 text-green-700 dark:text-green-400'
                            : inv.status === 'in_progress'
                            ? 'bg-blue-100 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400'
                            : 'bg-gray-100 dark:bg-gray-900/20 text-gray-700 dark:text-gray-400'
                        }`}
                      >
                        {inv.status}
                      </span>
                    </td>
                    <td className="px-6 py-4 text-sm text-[#64748B] dark:text-[#94A3B8]">
                      {new Date(inv.created_at).toLocaleDateString()}
                    </td>
                    <td className="px-6 py-4">
                      <button
                        onClick={() => navigate(`/investigations/${inv.id}`)}
                        className="text-[#4F46E5] dark:text-[#818CF8] hover:underline text-sm font-medium"
                      >
                        View Details
                      </button>
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
