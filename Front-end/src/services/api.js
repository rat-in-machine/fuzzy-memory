import axios from 'axios';

const API_BASE_URL = 'http://127.0.0.1:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const chatAPI = {
  // Buscar juegos por nombre
  searchByName: (name, limit = 5) =>
    api.get('/search-game', { params: { name, limit } }),

  // Buscar juegos por género
  searchByGenre: (genre, limit = 5) =>
    api.get('/search-by-genre', { params: { genre, limit } }),

  // Chat (recomendación)
  chat: (query, sessionId = null) =>
    api.post('/chat', { query, session_id: sessionId }),

  // Reset sesión
  resetChat: (sessionId) =>
    api.post('/chat/reset', null, { params: { session_id: sessionId } }),

  // Historial
  getChatHistory: (sessionId) =>
    api.get(`/chat/history/${sessionId}`),

  // Estadísticas
  getChatStats: (sessionId) =>
    api.get(`/chat/stats/${sessionId}`),
};

export default api;
