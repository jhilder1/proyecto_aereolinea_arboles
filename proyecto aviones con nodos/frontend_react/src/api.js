import axios from 'axios';

// Creamos la instancia apuntando al servidor backend FastAPI
const api = axios.create({
    baseURL: 'http://localhost:8000/api',
    headers: {
        'Content-Type': 'application/json'
    }
});

export default api;
