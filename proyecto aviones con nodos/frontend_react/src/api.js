import axios from 'axios';

// Create axios instance pointing to the FastAPI backend server
const api = axios.create({
    baseURL: 'http://localhost:8000/api',
    headers: {
        'Content-Type': 'application/json'
    }
});

export default api;
