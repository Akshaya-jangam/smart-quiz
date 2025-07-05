// src/services/api.js
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:5000',
});

export const generateQuiz = (data) => api.post('/generate', data);
export const getVersion = () => api.get('/version');
export const checkHealth = () => api.get('/health');