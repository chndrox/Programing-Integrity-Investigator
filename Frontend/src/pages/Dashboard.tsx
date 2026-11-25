import { useEffect, useState } from 'react'
import { dashboardAPI } from '../services/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts'

export default function Dashboard() {
  const [stats, setStats] = useState<any>(null)
  const [recentInvestigations, setRecentInvestigations] = useState<any[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [statsRes, recentRes] = await Promise.all([
          dashboardAPI.getStats(),
          dashboardAPI.getRecentInvestigations(),
        ])
        setStats(statsRes.data)
        setRecentInvestigations(recentRes.data)
      } catch (error) {
        console.error('Failed to fetch dashboard data:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [])

  const riskData = stats
    ? Object.entries(stats.risk_distribution).map(([key, value]) => ({
        name: key.charAt(0).toUpperCase() + key.slice(1),
        cases: value,
      }))
    : []

  if (loading) {
    return (
      <div className="flex items-center justify-center h-full">
        <div className="text-xl text-[#64748B] dark:text-[#94A3B8]">Loading dashboard...</div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      {/* Title */}
      <div>
        <h1 className="text-3xl font-bold text-[#0F172A] dark:text-[#F8FAFC]">
          Dashboard
        </h1>
        <p className="text-[#64748B] dark:text-[#94A3B8] mt-2">
          Overview of plagiarism investigations and submissions
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
        {stats && [
          {
            label: 'Total Submissions',
            value: stats.total_submissions,
            icon: '📤',
            color: 'bg-blue-100 dark:bg-blue-900/20 text-blue-700 dark:text-blue-400',
          },
          {
            label: 'Active Investigations',
            value: stats.active_investigations,
            icon: '🔍',
            color: 'bg-orange-100 dark:bg-orange-900/20 text-orange-700 dark:text-orange-400',
          },
          {
            label: 'Cases Under Review',
            value: stats.cases_requiring_review,
            icon: '⚠️',
            color: 'bg-red-100 dark:bg-red-900/20 text-red-700 dark:text-red-400',
          },
          {
            label: 'Completed',
            value: stats.completed_investigations,
            icon: '✓',
            color: 'bg-green-100 dark:bg-green-900/20 text-green-700 dark:text-green-400',
          },
        ].map((stat, idx) => (
          <div
            key={idx}
            className={`${stat.color} p-6 rounded-lg border border-current border-opacity-20`}
          >
            <div className="flex items-start justify-between">
              <div>
                <p className="text-sm font-medium opacity-75">{stat.label}</p>
                <p className="text-3xl font-bold mt-2">{stat.value}</p>
              </div>
              <span className="text-3xl">{stat.icon}</span>
            </div>
          </div>
        ))}
      </div>

      {/* Charts and Recent */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Risk Distribution */}
        <div className="lg:col-span-2 bg-white dark:bg-[#172033] rounded-lg border border-[#E2E8F0] dark:border-[#293548] p-6">
          <h2 className="text-xl font-bold text-[#0F172A] dark:text-[#F8FAFC] mb-4">
            Risk Distribution
          </h2>
          {riskData.length > 0 ? (
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={riskData}>
                <CartesianGrid
                  strokeDasharray="3 3"
                  stroke="#E2E8F0"
                  className="dark:stroke-[#293548]"
                />
                <XAxis dataKey="name" stroke="#64748B" className="dark:stroke-[#94A3B8]" />
                <YAxis stroke="#64748B" className="dark:stroke-[#94A3B8]" />
                <Tooltip
                  contentStyle={{
                    backgroundColor: '#F8FAFC',
                    border: '1px solid #E2E8F0',
                  }}
                  className="dark:bg-[#172033] dark:border-[#293548]"
                />
                <Bar dataKey="cases" fill="#4F46E5" className="dark:fill-[#818CF8]" />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-[300px] flex items-center justify-center text-[#64748B]">
              No data available
            </div>
          )}
        </div>

        {/* Recent Investigations */}
        <div className="bg-white dark:bg-[#172033] rounded-lg border border-[#E2E8F0] dark:border-[#293548] p-6">
          <h2 className="text-xl font-bold text-[#0F172A] dark:text-[#F8FAFC] mb-4">
            Recent Investigations
          </h2>
          <div className="space-y-3">
            {recentInvestigations.slice(0, 5).map((inv) => (
              <div
                key={inv.id}
                className="p-3 bg-[#F8FAFC] dark:bg-[#111827] rounded-lg border border-[#E2E8F0] dark:border-[#293548]"
              >
                <p className="text-sm font-medium text-[#0F172A] dark:text-[#F8FAFC]">
                  {inv.assignment_name}
                </p>
                <p className="text-xs text-[#64748B] dark:text-[#94A3B8] mt-1">
                  {inv.submission_count} submissions
                </p>
                <div className="flex items-center justify-between mt-2">
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
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}
