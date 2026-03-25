import { create } from 'zustand';

export const useAuthStore = create((set) => ({
  user: null,
  loading: true,
  setUser: (user) => set({ user }),
  setLoading: (loading) => set({ loading }),
  logout: () => set({ user: null }),
}));

export const useArticleStore = create((set) => ({
  articles: [],
  filteredArticles: [],
  selectedArticle: null,
  loading: false,
  error: null,
  
  setArticles: (articles) => set({ articles }),
  setFilteredArticles: (articles) => set({ filteredArticles: articles }),
  setSelectedArticle: (article) => set({ selectedArticle: article }),
  setLoading: (loading) => set({ loading }),
  setError: (error) => set({ error }),
}));

export const usePreferencesStore = create((set) => ({
  preferences: null,
  loading: false,
  
  setPreferences: (preferences) => set({ preferences }),
  setLoading: (loading) => set({ loading }),
}));
