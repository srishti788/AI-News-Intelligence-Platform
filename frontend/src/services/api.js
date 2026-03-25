import axios from 'axios';

const API_BASE = 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const newsAPI = {
  // Articles
  getArticles: (skip = 0, limit = 50, filters = {}) =>
    api.get('/articles', { params: { skip, limit, ...filters } }),
  
  getArticleDetail: (articleId) =>
    api.get(`/articles/${articleId}`),
  
  searchArticles: (query, limit = 50) =>
    api.get('/search', { params: { query, limit } }),
  
  // Summaries
  getSummary: (articleId, style = 'bullet') =>
    api.post('/summary', { article_id: articleId, style }),
  
  // Analysis
  analyzeArticle: (articleId) =>
    api.post('/analyze', null, { params: { article_id: articleId } }),
  
  // Chat
  chatWithAI: (question, userId = null) =>
    api.post('/chat', { question, user_id: userId }),
  
  // Recommendations
  getRecommendations: (userId, limit = 10) =>
    api.post('/recommendations', { user_id: userId, limit }),
  
  getSimilarArticles: (articleId, limit = 5) =>
    api.get(`/similar/${articleId}`, { params: { limit } }),
  
  // User Preferences
  setPreferences: (userId, preferences) =>
    api.post('/preferences', { user_id: userId, ...preferences }),
  
  getPreferences: (userId) =>
    api.get(`/preferences/${userId}`),
  
  // Health Check
  healthCheck: () =>
    api.get('/health'),
};

export default api;
