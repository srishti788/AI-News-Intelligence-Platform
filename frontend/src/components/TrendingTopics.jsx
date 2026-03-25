import React, { useState, useEffect } from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line } from 'recharts';
import { newsAPI } from '../services/api';

const TrendingTopics = () => {
  const [trendData, setTrendData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch articles and extract trending keywords
    const fetchTrends = async () => {
      try {
        const response = await newsAPI.getArticles(0, 100);
        const articles = response.data.articles;

        // Count keyword frequency (simplified)
        const keywordFreq = {};
        articles.forEach((article) => {
          const keywords = [article.category, article.source];
          keywords.forEach((keyword) => {
            keywordFreq[keyword] = (keywordFreq[keyword] || 0) + 1;
          });
        });

        const data = Object.entries(keywordFreq)
          .map(([name, value]) => ({ name, value }))
          .sort((a, b) => b.value - a.value)
          .slice(0, 10);

        setTrendData(data);
      } catch (error) {
        console.error('Error fetching trends:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchTrends();
  }, []);

  if (loading) {
    return <div className="text-gray-400">Loading trends...</div>;
  }

  return (
    <div className="bg-gradient-to-b from-dark-800 to-dark-900 rounded-2xl border border-glass-200 backdrop-blur-lg p-6">
      <h2 className="text-2xl font-bold text-white mb-6">Trending Topics</h2>
      <ResponsiveContainer width="100%" height={400}>
        <BarChart data={trendData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
          <XAxis dataKey="name" stroke="#9ca3af" />
          <YAxis stroke="#9ca3af" />
          <Tooltip
            contentStyle={{
              backgroundColor: '#1e293b',
              border: '1px solid #334155',
              borderRadius: '8px',
            }}
          />
          <Bar dataKey="value" fill="#3b82f6" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default TrendingTopics;
