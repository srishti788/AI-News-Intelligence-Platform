import React, { useState, useEffect } from 'react';
import { Send } from 'lucide-react';
import { newsAPI } from '../services/api';

const AIChat = ({ onTopicSearch }) => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm your AI News Assistant. Ask me anything about current news!",
      sender: 'bot',
      timestamp: new Date(),
    },
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim()) return;

    // Add user message
    const userMessage = {
      id: Date.now(),
      text: input,
      sender: 'user',
      timestamp: new Date(),
    };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const response = await newsAPI.chatWithAI(input);
      const botMessage = {
        id: Date.now() + 1,
        text: response.data.answer,
        sender: 'bot',
        timestamp: new Date(),
        articles: response.data.articles,
        topic: response.data.topic,
        numArticles: response.data.num_articles,
      };
      setMessages((prev) => [...prev, botMessage]);
      
      // Update news feed with the searched articles
      if (response.data.articles && response.data.articles.length > 0 && onTopicSearch) {
        // Pass articles in the format expected by the news feed
        onTopicSearch({
          articles: response.data.articles,
          query: response.data.topic,
          count: response.data.num_articles
        });
      }
    } catch (error) {
      console.error('Chat error:', error);
      const errorMessage = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'bot',
        timestamp: new Date(),
      };
      setMessages((prev) => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-gradient-to-b from-dark-800 to-dark-900 rounded-2xl border border-glass-200 backdrop-blur-lg p-6">
      <div className="flex-1 overflow-y-auto mb-6 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex ${message.sender === 'user' ? 'justify-end' : 'justify-start'}`}
          >
            <div className="w-full">
              <div
                className={`w-fit px-4 py-2 rounded-lg ${
                  message.sender === 'user'
                    ? 'ml-auto bg-blue-600 text-white'
                    : 'bg-glass-200 text-gray-100'
                }`}
              >
                <p className="text-sm">{message.text}</p>
                <span className="text-xs opacity-70 mt-1 block">
                  {message.timestamp.toLocaleTimeString()}
                </span>
              </div>
              
              {/* Show articles indicator */}
              {message.articles && message.articles.length > 0 && message.sender === 'bot' && (
                <div className="mt-2 text-xs text-blue-400">
                  📰 Found {message.numArticles} articles about "{message.topic}"
                </div>
              )}
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
            <div className="bg-glass-200 text-gray-100 px-4 py-2 rounded-lg">
              <div className="flex space-x-2">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-100"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-200"></div>
              </div>
            </div>
          </div>
        )}
      </div>

      <form onSubmit={handleSendMessage} className="flex gap-3">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about news, trends, or topics..."
          className="flex-1 px-4 py-2 bg-dark-700 border border-glass-200 rounded-lg text-white placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 disabled:opacity-50 text-white rounded-lg transition-colors flex items-center gap-2"
        >
          <Send size={18} />
        </button>
      </form>
    </div>
  );
};

export default AIChat;
