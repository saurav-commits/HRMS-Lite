import axios from 'axios';

// Ensure the API base URL includes /api
const API_BASE_URL = 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Employee API
export const employeeAPI = {
  getAll: () => api.get('/employees/'),
  create: (data) => api.post('/employees/', data),
  delete: (id) => api.delete(`/employees/${id}/`),
  get: (id) => api.get(`/employees/${id}/`),
};

// Attendance API
export const attendanceAPI = {
  getAll: (params = {}) => api.get('/attendance/', { params }),
  create: (data) => api.post('/attendance/', data),
  getSummary: (employeeId) => api.get(`/attendance/summary/${employeeId}/`),
};

export default api;
