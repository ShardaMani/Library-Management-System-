import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:5000', // Flask backend URL
  withCredentials: true, // Allows passing cookies or auth headers if needed
});

export default apiClient;
