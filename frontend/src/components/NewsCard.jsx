import React, { useState, useEffect } from 'react';
import { Heart, Share2, BookmarkPlus, ExternalLink } from 'lucide-react';
import { newsAPI } from '../services/api';

const NewsCard = ({ article, onSelect }) => {
  const [isFavorited, setIsFavorited] = useState(false);
  const [summary, setSummary] = useState(null);
  const [loadingSummary, setLoadingSummary] = useState(false);

  const handleGetSummary = async () => {
    if (summary) return;
    
    setLoadingSummary(true);
    try {
      const response = await newsAPI.getSummary(article.id);
      setSummary(response.data.summary);
    } catch (error) {
      console.error('Error getting summary:', error);
    } finally {
      setLoadingSummary(false);
    }
  };

  const handleShare = () => {
    if (navigator.share) {
      navigator.share({
        title: article.title,
        text: article.content.substring(0, 100),
        url: article.url,
      });
    }
  };

  return (
    <div
      onClick={() => onSelect(article)}
      className="group bg-gradient-to-br from-glass-100 to-glass-50 backdrop-blur-lg rounded-2xl border border-glass-200 p-6 hover:border-blue-500 transition-all duration-300 cursor-pointer transform hover:-translate-y-1 hover:shadow-xl"
    >
      {/* Header */}
      <div className="flex justify-between items-start mb-3">
        <div className="flex-1">
          <h3 className="text-xl font-bold text-white group-hover:text-blue-400 transition-colors">
            {article.title}
          </h3>
        </div>
        {article.sentiment && (
          <span
            className={`px-3 py-1 rounded-full text-xs font-semibold whitespace-nowrap ml-2 ${
              article.sentiment === 'positive'
                ? 'bg-green-900/40 text-green-300'
                : article.sentiment === 'negative'
                ? 'bg-red-900/40 text-red-300'
                : 'bg-yellow-900/40 text-yellow-300'
            }`}
          >
            {article.sentiment}
          </span>
        )}
      </div>

      {/* Metadata */}
      <div className="flex items-center gap-2 mb-4 text-sm text-gray-400">
        <span className="font-semibold text-blue-400">{article.source}</span>
        <span>•</span>
        <span>{new Date(article.published_at).toLocaleDateString()}</span>
      </div>

      {/* Content */}
      <p className="text-gray-300 mb-4 line-clamp-3">{article.content}</p>

      {/* Summary */}
      {summary && (
        <div className="bg-blue-900/20 border border-blue-700/30 rounded-lg p-3 mb-4">
          <p className="text-sm text-blue-200">{summary}</p>
        </div>
      )}

      {/* Actions */}
      <div className="flex items-center gap-3 mb-4">
        <button
          onClick={(e) => {
            e.stopPropagation();
            handleGetSummary();
          }}
          disabled={loadingSummary}
          className="text-sm px-3 py-1 bg-blue-600/20 hover:bg-blue-600/40 text-blue-300 rounded-lg transition-colors"
        >
          {loadingSummary ? 'Summarizing...' : 'Get AI Summary'}
        </button>
      </div>

      {/* Footer Actions */}
      <div className="flex justify-between items-center pt-4 border-t border-glass-200">
        <button
          onClick={(e) => {
            e.stopPropagation();
            setIsFavorited(!isFavorited);
          }}
          className={`p-2 rounded-lg transition-colors ${
            isFavorited
              ? 'bg-red-900/40 text-red-300'
              : 'hover:bg-glass-200 text-gray-400'
          }`}
        >
          <Heart size={18} fill={isFavorited ? 'currentColor' : 'none'} />
        </button>
        <a
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          onClick={(e) => e.stopPropagation()}
          className="flex items-center gap-2 text-blue-400 hover:text-blue-300 transition-colors"
        >
          Read Full Article
          <ExternalLink size={16} />
        </a>
        <button
          onClick={(e) => {
            e.stopPropagation();
            handleShare();
          }}
          className="p-2 rounded-lg hover:bg-glass-200 text-gray-400 transition-colors"
        >
          <Share2 size={18} />
        </button>
      </div>
    </div>
  );
};

export default NewsCard;
