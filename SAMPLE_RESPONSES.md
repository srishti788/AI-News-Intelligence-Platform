# Sample API Responses & Use Cases

## 📰 Sample News Data

### Sample Article Object
```json
{
  "id": "abc123def456",
  "title": "OpenAI Releases GPT-4 Turbo with 128K Context Window",
  "content": "In a groundbreaking announcement, OpenAI has released GPT-4 Turbo, featuring an unprecedented 128,000 token context window. This advancement allows the model to process and understand significantly longer documents and conversations, opening new possibilities for complex text analysis and generation tasks. The new model also introduces improved instruction following and reduced hallucinations compared to the previous version.",
  "url": "https://example.com/article/gpt4-turbo",
  "source": "TechCrunch",
  "source_url": "https://techcrunch.com",
  "author": "Jane Smith",
  "category": "Technology",
  "image_url": "https://example.com/images/gpt4.jpg",
  "published_at": "2024-01-15T10:30:00Z",
  "scraped_at": "2024-01-15T11:00:00Z",
  "processed_at": "2024-01-15T11:05:00Z",
  "sentiment": "positive",
  "keywords": [
    "artificial intelligence",
    "GPT-4",
    "OpenAI",
    "machine learning",
    "NLP"
  ],
  "content_hash": "hash123abc"
}
```

## 🤖 AI Processing Response Examples

### Summary Response
```json
{
  "status": "success",
  "article_id": "abc123def456",
  "summary": "• OpenAI releases GPT-4 Turbo with 128K context window\n• Enables processing of longer documents and conversations\n• Shows improved instruction following and reduced hallucinations",
  "style": "bullet",
  "model": "gpt-3.5-turbo",
  "success": true
}
```

### Analysis Response
```json
{
  "status": "success",
  "article_id": "abc123def456",
  "title": "OpenAI Releases GPT-4 Turbo with 128K Context Window",
  "sentiment": {
    "sentiment": "positive",
    "polarity": 0.8,
    "subjectivity": 0.4,
    "confidence": 0.8
  },
  "keywords": [
    "artificial intelligence",
    "GPT-4",
    "OpenAI",
    "machine learning",
    "language models",
    "NLP",
    "context window",
    "advancement"
  ]
}
```

### Chat Response
```json
{
  "status": "success",
  "question": "What are the major AI developments this week?",
  "answer": "Based on recent news articles, several major AI developments are trending this week:\n\n1. OpenAI released GPT-4 Turbo with a 128K context window, enabling the processing of significantly longer documents. This advancement improves instruction following and reduces hallucinations.\n\n2. Google announced new multimodal capabilities in their Bard AI assistant, allowing it to better understand and process different types of media.\n\n3. Meta released updates to their AI research tools, focusing on improving efficiency and reducing computational requirements.\n\nThese developments represent significant progress in making AI more capable and accessible.",
  "sources": 5,
  "timestamp": "2024-01-15T11:30:00Z"
}
```

## 📊 Recommendation Responses

### Personalized Recommendations
```json
{
  "status": "success",
  "user_id": "user-uuid-123",
  "count": 5,
  "recommendations": [
    {
      "id": "article-hash-1",
      "title": "AI Safety Concerns Addressed in New Framework",
      "content": "Researchers propose comprehensive AI safety framework...",
      "source": "Nature",
      "published_at": "2024-01-14T09:00:00Z",
      "recommendation_score": 0.95,
      "category": "Technology"
    },
    {
      "id": "article-hash-2",
      "title": "Machine Learning Applications in Healthcare",
      "content": "New study shows ML can improve diagnostic accuracy...",
      "source": "Science Daily",
      "published_at": "2024-01-13T14:20:00Z",
      "recommendation_score": 0.88,
      "category": "Science"
    },
    {
      "id": "article-hash-3",
      "title": "Deep Learning Breakthrough in Computer Vision",
      "content": "Researchers achieve new state-of-the-art results...",
      "source": "ArXiv",
      "published_at": "2024-01-12T16:45:00Z",
      "recommendation_score": 0.82,
      "category": "Technology"
    }
  ],
  "timestamp": "2024-01-15T11:35:00Z"
}
```

### Similar Articles
```json
{
  "status": "success",
  "article_id": "abc123def456",
  "count": 4,
  "similar_articles": [
    {
      "id": "article-hash-sim-1",
      "title": "GPT-4 Architecture Explained: What Makes It Different",
      "content": "Technical deep dive into GPT-4 architecture...",
      "source": "Medium",
      "author": "AI Researcher",
      "published_at": "2024-01-15T08:00:00Z",
      "similarity_score": 0.91,
      "category": "Technology"
    },
    {
      "id": "article-hash-sim-2",
      "title": "Comparing Language Models: GPT-4 vs Claude vs Gemini",
      "content": "Benchmark comparison of leading LLMs...",
      "source": "TechCrunch",
      "published_at": "2024-01-14T10:30:00Z",
      "similarity_score": 0.85,
      "category": "Technology"
    },
    {
      "id": "article-hash-sim-3",
      "title": "The Future of Large Language Models in 2024",
      "content": "Predictions and trends for LLM development...",
      "source": "Forbes",
      "published_at": "2024-01-13T15:00:00Z",
      "similarity_score": 0.78,
      "category": "Technology"
    },
    {
      "id": "article-hash-sim-4",
      "title": "How Enterprises Are Adopting GPT-4",
      "content": "Real-world implementations of GPT-4...",
      "source": "Forbes",
      "published_at": "2024-01-12T11:20:00Z",
      "similarity_score": 0.76,
      "category": "Business"
    }
  ],
  "timestamp": "2024-01-15T11:40:00Z"
}
```

## 👤 User Preferences

### Set Preferences
```json
{
  "status": "success",
  "user_id": "user-uuid-123",
  "preferences": {
    "interests": [
      "Artificial Intelligence",
      "Machine Learning",
      "Data Science",
      "Technology"
    ],
    "categories": [
      "Technology",
      "Science",
      "Research"
    ],
    "sentiment_filter": "all",
    "notification_enabled": true,
    "daily_digest_enabled": true,
    "digest_time": "09:00:00",
    "updated_at": "2024-01-15T11:45:00Z"
  }
}
```

### Get Preferences
```json
{
  "status": "success",
  "user_id": "user-uuid-123",
  "preferences": {
    "interests": [
      "Artificial Intelligence",
      "Machine Learning",
      "Data Science"
    ],
    "categories": [
      "Technology",
      "Science"
    ],
    "sentiment_filter": "all",
    "notification_enabled": true,
    "daily_digest_enabled": true,
    "digest_time": "09:00:00",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-15T11:45:00Z"
  }
}
```

## 📧 Email Responses

### Send Digest Email
```json
{
  "status": "success",
  "recipient": "user@example.com",
  "template_id": "daily_news_digest",
  "subject": "Daily News Digest - January 15, 2024",
  "email_id": "email-uuid-123",
  "timestamp": "2024-01-15T12:00:00Z",
  "delivery_status": "queued"
}
```

### Email Payload
```json
{
  "to": "user@example.com",
  "subject": "Daily News Digest - January 15, 2024",
  "template_id": "daily_news_digest",
  "variables": {
    "user_name": "John Doe",
    "articles_count": 10,
    "articles_html": "<div style='...'>Article cards HTML...</div>",
    "date": "January 15, 2024",
    "unsubscribe_url": "https://news-platform.com/unsubscribe?email=user@example.com"
  }
}
```

## 🔍 Search Results

### Search Response
```json
{
  "status": "success",
  "query": "artificial intelligence breakthrough",
  "count": 23,
  "articles": [
    {
      "id": "search-result-1",
      "title": "Major AI Breakthrough: Model Achieves Human-Level Performance",
      "content": "Researchers announce significant advancement in artificial intelligence...",
      "source": "TechCrunch",
      "author": "Tech Reporter",
      "published_at": "2024-01-15T09:30:00Z",
      "sentiment": "positive",
      "relevance_score": 0.98
    },
    {
      "id": "search-result-2",
      "title": "AI Safety Breakthrough Proposed by Leading Researchers",
      "content": "New framework for ensuring AI safety published...",
      "source": "Nature",
      "author": "Science Editor",
      "published_at": "2024-01-14T14:00:00Z",
      "sentiment": "neutral",
      "relevance_score": 0.94
    }
  ],
  "timestamp": "2024-01-15T12:05:00Z"
}
```

## 📈 Statistics & Analytics

### Platform Statistics
```json
{
  "status": "success",
  "statistics": {
    "total_articles": 15234,
    "articles_this_week": 2341,
    "articles_today": 287,
    "total_users": 5432,
    "active_users_today": 1234,
    "total_summaries": 8765,
    "total_recommendations": 45678,
    "trending_topics": [
      {
        "topic": "Artificial Intelligence",
        "count": 2345,
        "trend": "trending_up"
      },
      {
        "topic": "Climate Change",
        "count": 1234,
        "trend": "stable"
      },
      {
        "topic": "Technology",
        "count": 2123,
        "trend": "trending_up"
      }
    ],
    "sentiment_distribution": {
      "positive": 45,
      "neutral": 35,
      "negative": 20
    },
    "top_sources": [
      "TechCrunch",
      "Forbes",
      "CNN",
      "BBC",
      "Reuters"
    ]
  },
  "timestamp": "2024-01-15T12:10:00Z"
}
```

## 🚨 Error Response Examples

### 404 Not Found
```json
{
  "detail": "Article not found"
}
```

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters: 'limit' must be between 1 and 100"
}
```

### 500 Server Error
```json
{
  "detail": "An unexpected error occurred while processing your request. Please try again later."
}
```

### Rate Limit Exceeded
```json
{
  "detail": "Rate limit exceeded. Maximum 100 requests per minute allowed."
}
```

## 💡 Use Case Examples

### Use Case 1: News Dashboard
1. Call `GET /articles?limit=50` to get latest news
2. Call `GET /search?query=user_input` for search
3. Call `POST /recommendations` for personalized feed

### Use Case 2: Research Assistant
1. Call `POST /search` to find relevant articles
2. Call `POST /chat` to ask questions
3. Call `GET /similar/{article_id}` for related articles

### Use Case 3: Email Digest
1. Get user preferences: `GET /preferences/{user_id}`
2. Get recommendations: `POST /recommendations`
3. Format and send via Relay: `POST /email/send-digest`

### Use Case 4: Content Curation
1. Scrape feeds: `POST /scrape`
2. Analyze articles: `POST /analyze`
3. Store summaries: Auto-saved after summary generation

---

These examples demonstrate the API's capability to handle complex news intelligence tasks.
