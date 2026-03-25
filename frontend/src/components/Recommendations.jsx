import React, { useState, useEffect } from 'react';
import { newsAPI } from '../services/api';

const Recommendations = ({ userId }) => {
  const [recommendations, setRecommendations] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRecommendations = async () => {
      if (!userId) return;
      
      try {
        setLoading(true);
        const response = await newsAPI.getRecommendations(userId, 10);
        setRecommendations(response.data.recommendations);
      } catch (error) {
        console.error('Error fetching recommendations:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchRecommendations();
  }, [userId]);

  if (loading) {
    return <div className="text-gray-400">Loading recommendations...</div>;
  }

  return (
    <div className="bg-gradient-to-b from-dark-800 to-dark-900 rounded-2xl border border-glass-200 backdrop-blur-lg p-6">
      <h2 className="text-2xl font-bold text-white mb-6">For You</h2>
      <div className="space-y-4">
        {recommendations.map((article, idx) => (
          <div
            key={idx}
            className="p-4 bg-glass-100 rounded-lg border border-glass-200 hover:border-blue-500 transition-colors cursor-pointer"
          >
            <div className="flex justify-between items-start mb-2">
              <h4 className="font-semibold text-white flex-1">{article.title}</h4>
              <span className="text-xs bg-blue-600/40 text-blue-300 px-2 py-1 rounded">
                {Math.round((article.recommendation_score || 0) * 100)}%
              </span>
            </div>
            <p className="text-sm text-gray-400">{article.source}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Recommendations;
