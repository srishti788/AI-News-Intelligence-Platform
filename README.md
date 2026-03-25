# 🚀 AI-Powered News Intelligence Platform

A production-ready, full-stack platform that aggregates news from multiple sources, leverages AI for intelligent analysis, provides personalized recommendations, and delivers insights via a modern dashboard.

## 📋 Table of Contents

- [Features](#features)
- [Architecture](#architecture)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running Locally](#running-locally)
- [API Documentation](#api-documentation)
- [Deployment](#deployment)
- [Data Science Features](#data-science-features)
- [Contributing](#contributing)

## ✨ Features

### 🔍 News Aggregation
- Aggregates news from multiple RSS feeds
- Automatic scraping and data preprocessing
- Duplicate detection and content validation
- Real-time article updates

### 🤖 AI Capabilities
- **Summarization**: OpenAI-powered automatic summaries
- **Sentiment Analysis**: Polarity and sentiment detection
- **Keyword Extraction**: Key concepts identification
- **Q&A Interface**: Ask questions about news in natural language

### 📊 Machine Learning
- TF-IDF vectorization for content analysis
- Cosine similarity for article recommendations
- Personalized recommendation engine
- Trending topic detection

### 💬 Smart Features
- AI Chat Box for news queries
- Personalized "For You" section
- Similar articles discovery
- Smart filtering and search
- Real-time trending topics

### 📧 Communication
- Email digest automation via Relay.app
- Daily newsletter generation
- Breaking news alerts
- SMTP fallback support

### 🔐 User Management
- Supabase authentication
- User preferences and interests
- Activity tracking
- Personalized feeds

### 🎨 Modern UI
- Dark theme with glassmorphism
- Smooth animations
- Responsive design
- Real-time updates

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Data Sources                             │
│         (RSS Feeds, News APIs, YouTube)                     │
└────────────────┬────────────────────────────────────────────┘
                 │
                 ▼
┌─────────────────────────────────────────────────────────────┐
│          Python FastAPI Backend (Render)                     │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐        │
│  │  RSS     │ │  Data    │ │   AI     │ │   ML     │        │
│  │ Scraper  │ │Preprocess│ │ Process  │ │ Engine   │        │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘        │
│         │          │             │            │              │
│         └──────────┴─────────────┴────────────┘              │
│                     │                                        │
└─────────────────────┼────────────────────────────────────────┘
                      │
         ┌────────────┼────────────┐
         │            │            │
         ▼            ▼            ▼
    ┌────────┐  ┌──────────┐  ┌───────────┐
    │Supabase│  │ Relay.app│  │Redis Cache│
    │   DB   │  │Email Svc │  │ (Optional)│
    └────────┘  └──────────┘  └───────────┘
         │            │
         └────────────┼────────────┐
                      │            │
                      ▼            ▼
              ┌──────────────┐ ┌──────────┐
              │ React App    │ │  Email   │
              │ (Vercel/     │ │ Digests  │
              │  Render)     │ │          │
              └──────────────┘ └──────────┘
```

## 🛠️ Tech Stack

### Backend
- **Framework**: FastAPI (Python)
- **Database**: Supabase (PostgreSQL)
- **AI**: OpenAI API
- **ML**: scikit-learn (TF-IDF, cosine similarity)
- **Web Scraping**: feedparser
- **Email**: Relay.app + SMTP
- **Data Processing**: NLTK, TextBlob, pandas, numpy
- **Async**: aiohttp, asyncio
- **Caching**: Redis
- **Scheduling**: APScheduler

### Frontend
- **Framework**: React 18
- **Build**: Vite
- **Styling**: Tailwind CSS
- **State**: Zustand
- **HTTP**: Axios
- **Database**: Supabase JS client
- **Charts**: Recharts
- **Icons**: Lucide React
- **Animation**: Framer Motion

### DevOps
- **Containerization**: Docker
- **Orchestration**: Docker Compose
- **Backend Hosting**: Render
- **Frontend Hosting**: Render or Vercel
- **Database**: Supabase Cloud
- **CI/CD**: GitHub Actions (optional)

## 📦 Prerequisites

- Python 3.11+
- Node.js 18+
- Docker & Docker Compose
- Git
- Supabase account
- OpenAI API key
- Relay.app webhook URL (optional)

## 🔧 Installation

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/news-aggregator.git
cd news_aggregator
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt

# Copy and configure environment
cp .env.example .env
# Edit .env with your credentials
```

### 3. Frontend Setup
```bash
cd ../frontend

# Install dependencies
npm install --legacy-peer-deps

# Copy and configure environment
cp .env.example .env
# Edit .env with your credentials
```

## ⚙️ Configuration

### Backend (.env)
```env
# Server
DEBUG=false
HOST=0.0.0.0
PORT=8000

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key
SUPABASE_JWT_SECRET=your_jwt_secret

# OpenAI
OPENAI_API_KEY=sk-your-key
OPENAI_MODEL=gpt-3.5-turbo

# Relay.app (Optional)
RELAY_WEBHOOK_URL=https://relay.app/webhooks/your-webhook
RELAY_API_KEY=your_relay_key

# Email (SMTP Fallback)
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=your_email@gmail.com
```

### Frontend (.env.local)
```env
VITE_SUPABASE_URL=https://your-project.supabase.co
VITE_SUPABASE_ANON_KEY=your_anon_key
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

## 🚀 Running Locally

### Option 1: Docker Compose (Recommended)
```bash
# Create .env file in root with all credentials
docker-compose up --build

# Backend: http://localhost:8000
# Frontend: http://localhost:5173
# API Docs: http://localhost:8000/docs
```

### Option 2: Manual Run

**Terminal 1 - Backend**:
```bash
cd backend
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend**:
```bash
cd frontend
npm run dev
```

## 📚 API Documentation

### Base URL
```
http://localhost:8000/api/v1
```

### Key Endpoints

#### News Management
- `GET /articles` - Get articles with pagination
- `GET /articles/{article_id}` - Get article details
- `GET /search?query=...` - Search articles
- `POST /scrape` - Manually scrape RSS feeds

#### AI Features
- `POST /summary` - Generate AI summary
- `POST /analyze` - Analyze article
- `POST /chat` - Chat with AI about news

#### Recommendations
- `POST /recommendations` - Get personalized recommendations
- `GET /similar/{article_id}` - Get similar articles

#### User Management
- `POST /preferences` - Set user preferences
- `GET /preferences/{user_id}` - Get user preferences

#### Health
- `GET /health` - Health check

### Example Requests

**Get Articles**:
```bash
curl -X GET "http://localhost:8000/api/v1/articles?skip=0&limit=50"
```

**Search Articles**:
```bash
curl -X GET "http://localhost:8000/api/v1/search?query=ai&limit=20"
```

**Get Summary**:
```bash
curl -X POST "http://localhost:8000/api/v1/summary" \
  -H "Content-Type: application/json" \
  -d '{"article_id": "your_article_id", "style": "bullet"}'
```

**Chat with AI**:
```bash
curl -X POST "http://localhost:8000/api/v1/chat" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is trending in AI?"}'
```

## 🌐 Deployment

### Backend on Render

1. **Create Render Service**:
   - Go to https://render.com
   - Connect GitHub repository
   - Select "New Web Service"
   - Point to `backend` directory

2. **Configure Environment**:
   ```yaml
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

3. **Set Environment Variables**:
   - Add all variables from `.env.example`

### Frontend on Render

1. **Create Render Service**:
   - Select "Static Site" or "Web Service"
   - Point to `frontend` directory

2. **Configure**:
   ```yaml
   Build Command: npm install && npm run build
   Publish Directory: dist
   ```

### Frontend on Vercel

```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
cd frontend
vercel
```

### Database: Supabase Setup

1. **Create Tables**:
   - Run SQL from `backend/database_schema.sql`
   - In Supabase SQL Editor

2. **Enable Auth**:
   - Configure authentication in Supabase
   - Set redirect URLs

3. **Set up RLS**:
   - Enable Row Level Security
   - Configure policies for user privacy

## 📊 Data Science Features

### TF-IDF Vectorization
```python
from app.ml_engine.recommendation_engine import RecommendationEngine

# Create and train model
engine = RecommendationEngine()
engine.fit(articles)

# Get similar articles
similar = engine.get_similar_articles(article_id, top_k=5)
```

### Cosine Similarity
```python
# Calculate similarity between vectors
from app.ml_engine.recommendation_engine import SimilarityCalculator

similarity = SimilarityCalculator.cosine_similarity(vec1, vec2)
```

### Evaluation Metrics
```python
from app.ml_engine.recommendation_engine import MEvaluationMetrics

# Calculate coverage
coverage = MEvaluationMetrics.calculate_coverage(recommendations, total_items)

# Calculate diversity
diversity = MEvaluationMetrics.calculate_diversity(recommendations)

# Precision@K and Recall@K
precision = MEvaluationMetrics.calculate_precision_at_k(relevant, recommended, k=5)
recall = MEvaluationMetrics.calculate_recall_at_k(relevant, recommended, k=5)
```

## 📧 Email Integration (Relay.app)

### Webhook Configuration
```bash
# In Relay.app dashboard, create webhook pointing to:
POST https://your-backend.render.com/api/v1/email/send-digest
```

### Payload Format
```json
{
  "to": "user@example.com",
  "template_id": "daily_news_digest",
  "variables": {
    "user_name": "John",
    "articles_count": 10,
    "date": "2024-01-15"
  }
}
```

## 📈 Monitoring & Logging

### Backend Logs
```bash
# View logs on Render dashboard
# Or locally:
docker-compose logs -f backend
```

### Frontend Console
- Open browser DevTools (F12)
- Check Console for errors

### Database
- Monitor queries in Supabase dashboard
- Check Row Level Security policies

## 🧪 Testing

### Backend Tests
```bash
# Install pytest
pip install pytest pytest-asyncio

# Run tests
pytest tests/
```

### Frontend Tests
```bash
# Install testing library
npm install --save-dev @testing-library/react @testing-library/jest-dom

# Run tests
npm test
```

## 📝 Project Structure

```
news_aggregator/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py
│   │   ├── ai_processing/
│   │   │   └── ai_processor.py
│   │   ├── database/
│   │   │   └── supabase_client.py
│   │   ├── email_service/
│   │   │   └── relay_service.py
│   │   ├── ml_engine/
│   │   │   └── recommendation_engine.py
│   │   ├── scrapers/
│   │   │   └── rss_scraper.py
│   │   ├── utils/
│   │   │   └── data_preprocessor.py
│   │   ├── config.py
│   │   └── main.py
│   ├── requirements.txt
│   ├── .env.example
│   ├── Dockerfile
│   └── database_schema.sql
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── AIChat.jsx
│   │   │   ├── NewsFeed.jsx
│   │   │   ├── NewsCard.jsx
│   │   │   ├── TrendingTopics.jsx
│   │   │   ├── Recommendations.jsx
│   │   │   ├── SearchBar.jsx
│   │   │   └── Header.jsx
│   │   ├── hooks/
│   │   │   └── useAuth.js
│   │   ├── services/
│   │   │   ├── api.js
│   │   │   └── supabase.js
│   │   ├── stores/
│   │   │   └── store.js
│   │   ├── styles/
│   │   │   └── index.css
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── package.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── .env.example
│   ├── Dockerfile
│   └── index.html
├── docker-compose.yml
└── README.md
```

## 🔐 Security Best Practices

1. **Environment Variables**: Never commit `.env` files
2. **API Keys**: Rotate regularly
3. **CORS**: Configure only allowed origins
4. **RLS**: Enable Row Level Security on Supabase
5. **HTTPS**: Use only in production
6. **Rate Limiting**: Implement on API endpoints
7. **Input Validation**: Validate all user inputs
8. **Dependencies**: Regularly update packages

## 🐛 Troubleshooting

### Backend Issues
- Check logs: `docker-compose logs backend`
- Verify Supabase connection
- Test OpenAI API key
- Check Redis connection

### Frontend Issues
- Clear cache: `npm run build && npm run preview`
- Check browser console
- Verify API base URL
- Test API endpoints manually

### Database Issues
- Verify table creation
- Check RLS policies
- Monitor query performance
- Review error logs

## 📄 License

MIT License - see LICENSE file

## 🤝 Contributing

1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

## 📞 Support

For issues and questions:
1. Check GitHub Issues
2. Create new issue with details
3. Include logs and reproduction steps

---

Built with ❤️ for intelligent news consumption
