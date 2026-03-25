# API Documentation

## Base URL
```
http://localhost:8000/api/v1
```

## Authentication
The API uses Supabase JWT tokens for authentication. Include the token in the Authorization header:
```
Authorization: Bearer your_jwt_token
```

## Endpoints

### 📰 News Management

#### Get All Articles
```http
GET /articles
```

**Query Parameters:**
- `skip` (integer, default: 0) - Number of articles to skip
- `limit` (integer, default: 50, max: 100) - Number of articles to return
- `category` (string, optional) - Filter by category
- `sentiment` (string, optional) - Filter by sentiment (positive, negative, neutral)

**Response:**
```json
{
  "status": "success",
  "count": 50,
  "articles": [
    {
      "id": "article-hash",
      "title": "Breaking News Title",
      "content": "Article content...",
      "url": "https://...",
      "source": "TechCrunch",
      "author": "John Doe",
      "category": "Technology",
      "sentiment": "positive",
      "published_at": "2024-01-15T10:30:00",
      "image_url": "https://..."
    }
  ]
}
```

#### Get Article by ID
```http
GET /articles/{article_id}
```

**Response:**
```json
{
  "status": "success",
  "article": {...},
  "summary": {
    "id": "uuid",
    "article_id": "...",
    "summary": "AI-generated summary text",
    "style": "bullet",
    "sentiment": "positive"
  }
}
```

#### Search Articles
```http
GET /search
```

**Query Parameters:**
- `query` (string, required) - Search query
- `limit` (integer, default: 50) - Results limit

**Response:**
```json
{
  "status": "success",
  "query": "artificial intelligence",
  "count": 25,
  "articles": [...]
}
```

#### Scrape RSS Feeds
```http
POST /scrape
```

**Response:**
```json
{
  "status": "success",
  "articles_scraped": 150,
  "articles_stored": 145,
  "timestamp": "2024-01-15T10:30:00"
}
```

### 🤖 AI Processing

#### Generate Article Summary
```http
POST /summary
Content-Type: application/json

{
  "article_id": "article-hash",
  "style": "bullet"
}
```

**Style Options:**
- `bullet` - Bullet point format
- `paragraph` - Paragraph format
- `short` - One sentence summary

**Response:**
```json
{
  "status": "success",
  "article_id": "...",
  "summary": "• Key point 1\n• Key point 2\n• Key point 3",
  "model": "gpt-3.5-turbo"
}
```

#### Analyze Article
```http
POST /analyze?article_id=article-hash
```

**Response:**
```json
{
  "status": "success",
  "article_id": "...",
  "title": "Article Title",
  "sentiment": {
    "sentiment": "positive",
    "polarity": 0.75,
    "subjectivity": 0.45,
    "confidence": 0.75
  },
  "keywords": ["AI", "technology", "innovation", "machine learning", "future"]
}
```

#### Chat with AI
```http
POST /chat
Content-Type: application/json

{
  "question": "What's trending in AI?",
  "user_id": "optional-user-uuid"
}
```

**Response:**
```json
{
  "status": "success",
  "question": "What's trending in AI?",
  "answer": "Based on recent news articles, the trending topics in AI include...",
  "sources": 5
}
```

### 🎯 Recommendations

#### Get Personalized Recommendations
```http
POST /recommendations
Content-Type: application/json

{
  "user_id": "user-uuid",
  "limit": 10
}
```

**Response:**
```json
{
  "status": "success",
  "user_id": "...",
  "count": 10,
  "recommendations": [
    {
      "id": "article-hash",
      "title": "Article Title",
      "content": "...",
      "recommendation_score": 0.87,
      "source": "TechCrunch"
    }
  ]
}
```

#### Get Similar Articles
```http
GET /similar/{article_id}
```

**Query Parameters:**
- `limit` (integer, default: 5, max: 20) - Number of similar articles

**Response:**
```json
{
  "status": "success",
  "article_id": "...",
  "count": 5,
  "similar_articles": [
    {
      "id": "...",
      "title": "...",
      "similarity_score": 0.82,
      "source": "..."
    }
  ]
}
```

### 👤 User Preferences

#### Set User Preferences
```http
POST /preferences
Content-Type: application/json

{
  "user_id": "user-uuid",
  "interests": ["AI", "Technology", "Science"],
  "categories": ["News", "Technology"],
  "sentiment_filter": "all"
}
```

**Response:**
```json
{
  "status": "success",
  "user_id": "...",
  "preferences": {
    "interests": ["AI", "Technology", "Science"],
    "categories": ["News", "Technology"],
    "sentiment_filter": "all",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

#### Get User Preferences
```http
GET /preferences/{user_id}
```

**Response:**
```json
{
  "status": "success",
  "user_id": "...",
  "preferences": {
    "interests": ["AI", "Technology", "Science"],
    "categories": ["News", "Technology"],
    "sentiment_filter": "all"
  }
}
```

### ❤️ Health Check

#### Health Check
```http
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-15T10:30:00",
  "service": "News Intelligence Platform API"
}
```

## Error Responses

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters"
}
```

### 404 Not Found
```json
{
  "detail": "Article not found"
}
```

### 500 Internal Server Error
```json
{
  "detail": "An error occurred while processing your request"
}
```

## Rate Limiting

- 100 requests per minute per API key
- Rate limit headers: `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset`

## Example cURL Commands

### Get Articles
```bash
curl -X GET "http://localhost:8000/api/v1/articles?skip=0&limit=10"
```

### Search Articles
```bash
curl -X GET "http://localhost:8000/api/v1/search?query=ai&limit=20"
```

### Get Summary
```bash
curl -X POST "http://localhost:8000/api/v1/summary" \
  -H "Content-Type: application/json" \
  -d '{
    "article_id": "abc123",
    "style": "bullet"
  }'
```

### Chat with AI
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "question": "What is trending in AI?"
  }'
```

### Get Recommendations
```bash
curl -X POST "http://localhost:8000/api/v1/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-uuid-123",
    "limit": 10
  }'
```

### Get Similar Articles
```bash
curl -X GET "http://localhost:8000/api/v1/similar/article-hash?limit=5"
```

### Set User Preferences
```bash
curl -X POST "http://localhost:8000/api/v1/preferences" \
  -H "Content-Type: application/json" \
  -d '{
    "user_id": "user-uuid-123",
    "interests": ["AI", "Technology"],
    "categories": ["News", "Technology"]
  }'
```

## Response Format

All successful responses follow this format:
```json
{
  "status": "success",
  "data": {
    "...": "..."
  }
}
```

All error responses follow this format:
```json
{
  "status": "error",
  "message": "Error description",
  "detail": "Additional error details"
}
```

## Data Models

### Article
```python
{
  "id": str,                  # Unique identifier
  "title": str,               # Article title
  "content": str,             # Article content/summary
  "url": str,                 # URL to full article
  "source": str,              # News source
  "source_url": str,          # News source URL
  "author": str,              # Article author
  "category": str,            # Article category
  "image_url": str,           # Article image
  "published_at": datetime,   # Publication time
  "scraped_at": datetime,     # When scraped
  "sentiment": str,           # positive/negative/neutral
  "keywords": list[str]       # Extracted keywords
}
```

### Summary
```python
{
  "id": str,              # UUID
  "article_id": str,      # Reference article
  "summary": str,         # AI-generated summary
  "style": str,           # bullet/paragraph/short
  "keywords": list[str],  # Key terms
  "sentiment": str,       # Sentiment of content
}
```

### User Preferences
```python
{
  "user_id": str,           # User UUID
  "interests": list[str],   # User interests
  "categories": list[str],  # Preferred categories
  "sentiment_filter": str,  # positive/negative/all
  "updated_at": datetime    # Last update
}
```
