import React, { useState, useEffect } from 'react';
import Header from './components/Header';
import SearchBar from './components/SearchBar';
import NewsFeed from './components/NewsFeed';
import AIChat from './components/AIChat';
import TrendingTopics from './components/TrendingTopics';
import Recommendations from './components/Recommendations';
import { useAuth } from './hooks/useAuth';
import { authService } from './services/supabase';
import './styles/index.css';

function App() {
  const { user, loading } = useAuth();
  const [selectedArticle, setSelectedArticle] = useState(null);
  const [searchResults, setSearchResults] = useState(null);
  const [demoMode, setDemoMode] = useState(false);

  const handleLogout = async () => {
    await authService.signOut();
    setDemoMode(false);
  };

  const handleDemoMode = () => {
    setDemoMode(true);
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-900 flex items-center justify-center">
        <div className="text-white">Loading...</div>
      </div>
    );
  }

  if (!user && !demoMode) {
    return (
      <div className="min-h-screen bg-gradient-to-b from-dark-900 to-dark-800 flex items-center justify-center p-4">
        <div className="max-w-md w-full">
          <div className="bg-gradient-to-b from-dark-800 to-dark-900 rounded-2xl border border-glass-200 backdrop-blur-lg p-8 text-center">
            <div className="text-4xl mb-4">📰</div>
            <h1 className="text-3xl font-bold text-white mb-2">News Intelligence</h1>
            <p className="text-gray-400 mb-6">Sign in to access AI-powered news insights</p>
            
            <div className="space-y-4">
              <p className="text-sm text-gray-500">Demo Mode: View trending news without login</p>
              <button
                onClick={handleDemoMode}
                className="w-full px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg font-semibold transition-colors"
              >
                Continue to Dashboard
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-b from-dark-900 via-dark-800 to-dark-900">
      <Header user={user} demoMode={demoMode} onLogout={handleLogout} />

      <main className="max-w-7xl mx-auto px-6 py-12">
        {/* Search Bar */}
        <div className="mb-12">
          <SearchBar onSearchResults={setSearchResults} />
        </div>

        {/* Main Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Left Column - News Feed */}
          <div className="lg:col-span-2">
            <NewsFeed searchResults={searchResults} selectedArticle={selectedArticle} onSelectArticle={setSelectedArticle} />
          </div>

          {/* Right Column - Sidebar */}
          <div className="space-y-8">
            {/* AI Chat */}
            <div className="h-96">
              <AIChat onTopicSearch={setSearchResults} />
            </div>

            {/* Recommendations */}
            <Recommendations userId={user?.id || 'demo-user'} />
          </div>
        </div>

        {/* Trending Topics - Full Width */}
        <div className="mt-12">
          <TrendingTopics />
        </div>

        {/* Article Detail Modal */}
        {selectedArticle && (
          <div
            className="fixed inset-0 bg-black/50 backdrop-blur-sm flex items-center justify-center p-4 z-50"
            onClick={() => setSelectedArticle(null)}
          >
            <div
              className="bg-dark-800 rounded-2xl border border-glass-200 max-w-2xl w-full max-h-96 overflow-y-auto"
              onClick={(e) => e.stopPropagation()}
            >
              <div className="p-8">
                <h2 className="text-2xl font-bold text-white mb-4">{selectedArticle.title}</h2>
                <p className="text-gray-400 mb-4">
                  {selectedArticle.source} • {new Date(selectedArticle.published_at).toLocaleDateString()}
                </p>
                <p className="text-gray-300 mb-6">{selectedArticle.content}</p>
                <a
                  href={selectedArticle.url}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="inline-block px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
                >
                  Read Full Article
                </a>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
