import axios from 'axios';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL;
const API_BASE = `${BACKEND_URL}/api`;

// Create axios instance with default config
const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add response interceptor for error handling
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export const portfolioApi = {
  // Personal Information
  getPersonalInfo: () => apiClient.get('/personal-info'),
  updatePersonalInfo: (data) => apiClient.put('/personal-info', data),
  
  // Skills
  getSkills: () => apiClient.get('/skills'),
  createSkill: (data) => apiClient.post('/skills', data),
  updateSkill: (id, data) => apiClient.put(`/skills/${id}`, data),
  deleteSkill: (id) => apiClient.delete(`/skills/${id}`),
  
  // Experience  
  getExperience: () => apiClient.get('/experience'),
  createExperience: (data) => apiClient.post('/experience', data),
  updateExperience: (id, data) => apiClient.put(`/experience/${id}`, data),
  deleteExperience: (id) => apiClient.delete(`/experience/${id}`),
  
  // Education
  getEducation: () => apiClient.get('/education'),
  createEducation: (data) => apiClient.post('/education', data),
  updateEducation: (id, data) => apiClient.put(`/education/${id}`, data),
  deleteEducation: (id) => apiClient.delete(`/education/${id}`),
  
  // Languages
  getLanguages: () => apiClient.get('/languages'),
  createLanguage: (data) => apiClient.post('/languages', data),
  updateLanguage: (id, data) => apiClient.put(`/languages/${id}`, data),
  deleteLanguage: (id) => apiClient.delete(`/languages/${id}`),
  
  // Contact
  submitContact: (data) => apiClient.post('/contact', data),
  getContactMessages: () => apiClient.get('/contact'),
  
  // Health check
  healthCheck: () => apiClient.get('/'),
};

export default portfolioApi;