import { useEffect, useState } from 'react'
import { submissionsAPI } from '../services/api'

export default function Submissions() {
  const [submissions, setSubmissions] = useState<any[]>([])
  const [loading, setLoading] = useState(true)
  const [uploadLoading, setUploadLoading] = useState(false)

  useEffect(() => {
    fetchSubmissions()
  }, [])

  const fetchSubmissions = async () => {
    try {
      const response = await submissionsAPI.list()
      setSubmissions(response.data)
    } catch (error) {
      console.error('Failed to fetch submissions:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleFileUpload = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setUploadLoading(true)

    const formData = new FormData(e.currentTarget)

    try {
      await submissionsAPI.upload(formData)
      alert('Submission uploaded successfully!')
      fetchSubmissions()
      e.currentTarget.reset()
    } catch (error) {
      alert('Failed to upload submission')
      console.error(error)
    } finally {
      setUploadLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-[#0F172A] dark:text-[#F8FAFC]">Submissions</h1>
        <p className="text-[#64748B] dark:text-[#94A3B8] mt-2">
          Manage programming assignment submissions
        </p>
      </div>

      {/* Upload Form */}
      <div className="bg-white dark:bg-[#172033] rounded-lg border border-[#E2E8F0] dark:border-[#293548] p-6">
        <h2 className="text-lg font-bold text-[#0F172A] dark:text-[#F8FAFC] mb-4">
          Upload New Submission
        </h2>
        <form onSubmit={handleFileUpload} className="space-y-4">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <input
              type="number"
              name="student_id"
              placeholder="Student ID"
              required
              className="px-4 py-2 border border-[#E2E8F0] dark:border-[#293548] rounded-lg bg-white dark:bg-[#111827] text-[#0F172A] dark:text-[#F8FAFC]"
              disabled={uploadLoading}
            />
            <input
              type="number"
              name="assignment_id"
              placeholder="Assignment ID"
              required
              className="px-4 py-2 border border-[#E2E8F0] dark:border-[#293548] rounded-lg bg-white dark:bg-[#111827] text-[#0F172A] dark:text-[#F8FAFC]"
              disabled={uploadLoading}
            />
          </div>
          <input
            type="file"
            name="file"
            accept=".py,.java,.cpp,.js,.ts"
            required
            className="block w-full text-sm text-[#64748B] dark:text-[#94A3B8]
              file:px-4 file:py-2 file:rounded-lg file:border-0
              file:text-sm file:font-medium
              file:bg-[#4F46E5] dark:file:bg-[#818CF8] file:text-white
              hover:file:bg-[#4338CA] dark:hover:file:bg-[#6366F1]"
            disabled={uploadLoading}
          />
          <button
            type="submit"
            disabled={uploadLoading}
            className="w-full bg-[#4F46E5] dark:bg-[#818CF8] text-white py-2 rounded-lg font-medium hover:bg-[#4338CA] dark:hover:bg-[#6366F1] disabled:opacity-50"
          >
            {uploadLoading ? 'Uploading...' : 'Upload Submission'}
          </button>
        </form>
      </div>

      {/* Submissions List */}
      <div className="bg-white dark:bg-[#172033] rounded-lg border border-[#E2E8F0] dark:border-[#293548] overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className={`${
              true ? 'bg-[#F8FAFC] dark:bg-[#111827]' : 'bg-[#F8FAFC]'
            } border-b border-[#E2E8F0] dark:border-[#293548]`}>
              <tr>
                <th className="px-6 py-3 text-left text-sm font-semibold text-[#0F172A] dark:text-[#F8FAFC]">
                  Student
                </th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-[#0F172A] dark:text-[#F8FAFC]">
                  Assignment
                </th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-[#0F172A] dark:text-[#F8FAFC]">
                  File
                </th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-[#0F172A] dark:text-[#F8FAFC]">
                  Lines
                </th>
                <th className="px-6 py-3 text-left text-sm font-semibold text-[#0F172A] dark:text-[#F8FAFC]">
                  Submitted
                </th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={5} className="px-6 py-4 text-center text-[#64748B]">
                    Loading...
                  </td>
                </tr>
              ) : submissions.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-6 py-4 text-center text-[#64748B]">
                    No submissions yet
                  </td>
                </tr>
              ) : (
                submissions.map((submission) => (
                  <tr
                    key={submission.id}
                    className={`border-b border-[#E2E8F0] dark:border-[#293548] hover:bg-[#F8FAFC] dark:hover:bg-[#111827]`}
                  >
                    <td className="px-6 py-4 text-sm text-[#0F172A] dark:text-[#F8FAFC]">
                      {submission.student_name}
                    </td>
                    <td className="px-6 py-4 text-sm text-[#0F172A] dark:text-[#F8FAFC]">
                      {submission.assignment_name}
                    </td>
                    <td className="px-6 py-4 text-sm text-[#64748B] dark:text-[#94A3B8]">
                      {submission.file_name}
                    </td>
                    <td className="px-6 py-4 text-sm text-[#0F172A] dark:text-[#F8FAFC]">
                      {submission.source_code_lines}
                    </td>
                    <td className="px-6 py-4 text-sm text-[#64748B] dark:text-[#94A3B8]">
                      {new Date(submission.submitted_at).toLocaleDateString()}
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
