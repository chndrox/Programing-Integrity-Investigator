export default function Reports() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-[#0F172A] dark:text-[#F8FAFC]">Case Reports</h1>
        <p className="text-[#64748B] dark:text-[#94A3B8] mt-2">
          Review and approve investigation reports
        </p>
      </div>
      <div className="bg-white dark:bg-[#172033] rounded-lg border border-[#E2E8F0] dark:border-[#293548] p-6 text-center py-12">
        <p className="text-[#64748B] dark:text-[#94A3B8]">No reports yet</p>
      </div>
    </div>
  )
}
