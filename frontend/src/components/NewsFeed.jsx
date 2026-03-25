import React, { useState, useEffect } from 'react';
import NewsCard from './NewsCard';
import { newsAPI } from '../services/api';

const NewsFeed = ({ searchResults, selectedArticle, onSelectArticle }) => {
  const [articles, setArticles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [page, setPage] = useState(0);
  const [currentQuery, setCurrentQuery] = useState(null);

  // When search results are provided (from chat or search), use those
  useEffect(() => {
    if (searchResults && searchResults.articles && searchResults.articles.length > 0) {
      setArticles(searchResults.articles);
      setCurrentQuery(searchResults.query);
      setPage(0);
      setLoading(false);
    } else {
      // Load default articles
      fetchArticles();
    }
  }, [searchResults]);

  const fetchArticles = async () => {
    try {
      setLoading(true);
      const response = await newsAPI.getArticles(page * 50, 50);
      setArticles(response.data.articles || response.data);
      setCurrentQuery(null);
    } catch (error) {
      console.error('Error fetching articles:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    // Only fetch if not using search results
    if (!searchResults || !searchResults.articles) {
      fetchArticles();
    }
  }, [page, searchResults]);

  if (loading && !articles.length) {
    return <div className="text-gray-400">Loading news feed...</div>;
  }

  return (
    <div className="space-y-4">
      <div className="flex justify-between items-center">
        <div>
          <h2 className="text-2xl font-bold text-white">News Feed</h2>
          {currentQuery && (
            <p className="text-sm text-blue-400 mt-1">
              📰 Showing results for: <span className="font-semibold">"{currentQuery}"</span>
            </p>
          )}
        </div>
        <div className="flex gap-2">
          <button
            onClick={() => setPage(Math.max(0, page - 1))}
            disabled={page === 0 || currentQuery}
            className="px-4 py-2 bg-blue-600/20 text-blue-300 rounded-lg disabled:opacity-50 hover:bg-blue-600/40 transition-colors"
          >
            Previous
          </button>
          <button
            onClick={() => setPage(page + 1)}
            disabled={currentQuery}
            className="px-4 py-2 bg-blue-600/20 text-blue-300 rounded-lg hover:bg-blue-600/40 transition-colors disabled:opacity-50"
          >
            Next
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {articles.map((article) => (
          <NewsCard
            key={article.id || article.url}
            article={article}
            onSelect={onSelectArticle}
            isSelected={selectedArticle?.id === article.id}
          />
        ))}
      </div>

      {loading && <div className="text-center text-gray-400">Loading more articles...</div>}
      
      {articles.length === 0 && !loading && (
        <div className="text-center text-gray-400 py-8">
          No articles found. Try searching for a different topic.
        </div>
      )}
    </div>
  );
};

export default NewsFeed;
