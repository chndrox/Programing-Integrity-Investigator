import axios from 'axios'

const API_BASE_URL = 'http://localhost:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const authAPI = {
  login: (username: string, password: string) =>
    api.post('/auth/login', { username, password }),
  register: (data: any) => api.post('/auth/register', data),
}

export const dashboardAPI = {
  getStats: () => api.get('/dashboard/stats'),
  getRecentInvestigations: () => api.get('/dashboard/recent-investigations'),
}

export const submissionsAPI = {
  upload: (formData: FormData) =>
    api.post('/submissions/upload', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    }),
  list: (params?: any) => api.get('/submissions', { params }),
  get: (id: number) => api.get(`/submissions/${id}`),
  delete: (id: number) => api.delete(`/submissions/${id}`),
}

export const investigationsAPI = {
  start: (data: any) => api.post('/investigations/start', data),
  list: () => api.get('/investigations'),
  get: (id: number) => api.get(`/investigations/${id}`),
  getReport: (id: number) => api.get(`/investigations/${id}/report`),
}

export const reportsAPI = {
  list: () => api.get('/reports'),
  approve: (id: number, notes?: string) =>
    api.post(`/reports/${id}/approve`, { notes }),
}

export const mcpAPI = {
  getStatus: () => api.get('/mcp/status'),
}

export const settingsAPI = {
  get: () => api.get('/settings'),
  update: (data: any) => api.put('/settings', data),
}

export const auditAPI = {
  getLogs: (limit?: number) =>
    api.get('/audit-logs', { params: { limit } }),
}

export default api
