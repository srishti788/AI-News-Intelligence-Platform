# 🚀 Quick Reference Guide

## 📋 File Locations & Purposes

### Backend Core Files
| File | Location | Purpose |
|------|----------|---------|
| Main App | `backend/app/main.py` | FastAPI application entry point |
| API Routes | `backend/app/api/routes.py` | All 20+ REST endpoints |
| Config | `backend/app/config.py` | Settings from environment |
| Database | `backend/app/database/supabase_client.py` | Supabase operations |
| RSS Scraper | `backend/app/scrapers/rss_scraper.py` | Feed fetching & parsing |
| Data Prep | `backend/app/utils/data_preprocessor.py` | Text cleaning & validation |
| AI Processor | `backend/app/ai_processing/ai_processor.py` | OpenAI integration |
| ML Engine | `backend/app/ml_engine/recommendation_engine.py` | TF-IDF & recommendations |
| Email Service | `backend/app/email_service/relay_service.py` | Email & webhooks |

### Frontend Core Files
| File | Location | Purpose |
|------|----------|---------|
| Main App | `frontend/src/App.jsx` | React application |
| AI Chat | `frontend/src/components/AIChat.jsx` | Chat interface |
| News Feed | `frontend/src/components/NewsFeed.jsx` | Article list |
| News Card | `frontend/src/components/NewsCard.jsx` | Article card |
| Trends | `frontend/src/components/TrendingTopics.jsx` | Visualization |
| Sidebar | `frontend/src/components/Recommendations.jsx` | Suggestions |
| API Service | `frontend/src/services/api.js` | Backend API calls |
| Auth Service | `frontend/src/services/supabase.js` | Supabase auth |
| Styling | `frontend/src/styles/index.css` | Custom CSS |

### Config & Setup Files
| File | Purpose |
|------|---------|
| `backend/.env.example` | Backend config template |
| `backend/requirements.txt` | Python dependencies |
| `backend/Dockerfile` | Docker image for backend |
| `backend/database_schema.sql` | Database table creation |
| `frontend/.env.example` | Frontend config template |
| `frontend/package.json` | NPM dependencies |
| `frontend/vite.config.js` | Vite build config |
| `frontend/tailwind.config.js` | Tailwind CSS config |
| `docker-compose.yml` | Multi-container setup |

### Documentation Files
| File | Content |
|------|---------|
| `README.md` | Project overview & features |
| `API_DOCUMENTATION.md` | Complete API reference |
| `DEPLOYMENT.md` | Step-by-step deployment |
| `SAMPLE_RESPONSES.md` | API response examples |
| `PROJECT_SUMMARY.md` | What was built |

## 🔧 Common Commands

### Setup
```bash
# Backend setup
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env

# Frontend setup
cd frontend
npm install --legacy-peer-deps
cp .env.example .env.local
```

### Development
```bash
# Run backend
cd backend
uvicorn app.main:app --reload

# Run frontend
cd frontend
npm run dev

# Watch mode
npm run dev

# Docker
docker-compose up --build
```

### Build & Deploy
```bash
# Backend build
docker build -t news-backend ./backend

# Frontend build
cd frontend
npm run build

# Docker compose
docker-compose up -d
```

## 🔑 Critical Configuration Steps

### 1. Supabase Setup
```bash
# Create account at supabase.com
# Copy these credentials to .env:
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_public_key
SUPABASE_JWT_SECRET=your_jwt_secret

# Run SQL schema in Supabase SQL Editor:
# Paste content from backend/database_schema.sql
```

### 2. OpenAI Setup
```bash
# Get API key from openai.com
OPENAI_API_KEY=sk-your-key-here
OPENAI_MODEL=gpt-3.5-turbo
```

### 3. Relay.app Setup (Optional)
```bash
# Create account at relay.app
# Create webhook and copy:
RELAY_WEBHOOK_URL=https://relay.app/webhooks/...
RELAY_API_KEY=your_relay_key
```

### 4. Email Setup (Optional SMTP)
```bash
# For Gmail, use App Password:
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=your_email@gmail.com
```

## 📊 Data Flow Diagram

```
RSS Feeds
    ↓
[Scraper] → Articles
    ↓
[Preprocessor] → Clean Data
    ↓
[AI Processor] → Summaries, Sentiment
    ↓
[ML Engine] → Vectors, Similarity
    ↓
[Database] → Store Everything
    ↓
[API Routes] → Serve Data
    ↓
[Frontend] → Display
    ↓
[Email Service] → Digest Emails
```

## 🎯 Key Algorithms

### TF-IDF Recommendation
1. Vectorize article text using TF-IDF
2. Calculate cosine similarity between vectors
3. Rank by similarity score
4. Return top-K results

### Sentiment Analysis
1. Text preprocessing
2. TextBlob polarity analysis (-1 to 1)
3. Classify as positive/negative/neutral
4. Calculate confidence score

### Article Similarity
1. Fit TF-IDF model on all articles
2. Calculate cosine similarity matrix
3. Filter by threshold (0.3 default)
4. Sort by score and return

## 📡 API Quick Reference

### Most Used Endpoints
```bash
# Get news
GET /api/v1/articles?limit=50

# Search
GET /api/v1/search?query=ai

# Get summary
POST /api/v1/summary -d '{"article_id":"..."}'

# Chat with AI
POST /api/v1/chat -d '{"question":"..."}'

# Get recommendations
POST /api/v1/recommendations -d '{"user_id":"..."}'

# Get similar
GET /api/v1/similar/{article_id}

# Health check
GET /api/v1/health
```

## 🐛 Troubleshooting Quick Guide

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError` | Run `pip install -r requirements.txt` |
| `SUPABASE connection failed` | Check SUPABASE_URL and SUPABASE_KEY |
| `OPENAI API error` | Verify OPENAI_API_KEY and check quota |
| `Frontend blank page` | Check browser console, verify API URL |
| `Port 8000 already in use` | Use `uvicorn app.main:app --port 8001` |
| `npm install fails` | Use `npm install --legacy-peer-deps` |
| `Docker build fails` | Clear cache: `docker system prune` |

## 📈 Performance Tips

### Backend
- Enable Redis caching
- Use connection pooling
- Index frequently queried columns
- Batch API calls when possible
- Implement rate limiting

### Frontend
- Enable code splitting
- Lazy load components
- Optimize images
- Use React.memo for expensive components
- Enable service workers

### Database
- Create indices on foreign keys
- Monitor slow queries
- Archive old articles (> 6 months)
- Use pagination for large datasets

## 🔐 Security Checklist

- [ ] Never commit .env files
- [ ] Rotate OPENAI_API_KEY every 90 days
- [ ] Enable HTTPS in production
- [ ] Set CORS to specific origins only
- [ ] Enable RLS on Supabase tables
- [ ] Use strong passwords for admin accounts
- [ ] Validate all user inputs
- [ ] Rate limit API endpoints
- [ ] Log security events
- [ ] Monitor failed login attempts

## 📚 Learning Resources

### FastAPI
- Official Docs: https://fastapi.tiangolo.com
- Tutorial: https://fastapi.tiangolo.com/tutorial/first-steps/
- Advanced: https://fastapi.tiangolo.com/advanced/

### React
- Official Docs: https://react.dev
- Hooks Guide: https://react.dev/reference/react/hooks
- Performance Tips: https://react.dev/learn/render-and-commit

### Supabase
- Getting Started: https://supabase.com/docs
- Auth Guide: https://supabase.com/docs/guides/auth
- Realtime: https://supabase.com/docs/guides/realtime

### Machine Learning
- TF-IDF: https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf
- Cosine Similarity: https://scikit-learn.org/stable/modules/generated/sklearn.metrics.pairwise.cosine_similarity.html

## 🎓 Architecture Patterns Used

1. **MVC Architecture**: Models, Views, Controllers separation
2. **Service Layer Pattern**: Abstraction of business logic
3. **Repository Pattern**: Data access abstraction
4. **Singleton Pattern**: Database connection management
5. **Factory Pattern**: Object creation
6. **Strategy Pattern**: Different AI/ML algorithms
7. **Observer Pattern**: Event-driven updates
8. **Middleware Pattern**: Request processing pipeline

## 💾 Backup & Recovery

### Backup Database
```bash
# Export Supabase data
# In Supabase dashboard → Data → Export
# Or use Supabase CLI: supabase db pull
```

### Restore from Backup
```bash
# Push SQL schema: supabase db push
# Restore data manually or via API
```

## 📊 Production Deployment Checklist

- [ ] Environment variables set correctly
- [ ] Database schema created and seeded
- [ ] Redis instance configured (optional)
- [ ] CORS properly configured
- [ ] SSL certificates valid
- [ ] DNS records pointing correctly
- [ ] Monitoring and alerts set up
- [ ] Error logging enabled
- [ ] Rate limiting configured
- [ ] Backup strategy implemented
- [ ] Load testing completed
- [ ] Documentation updated
- [ ] API documentation published
- [ ] User support plan ready
- [ ] Incident response plan ready

## 🚀 Ready to Launch!

You now have a **complete, production-ready platform** with:
- ✅ Full backend API
- ✅ Modern React frontend
- ✅ Cloud database
- ✅ AI integration
- ✅ ML recommendations
- ✅ Email service
- ✅ Docker support
- ✅ Comprehensive docs

**Next Step**: Configure your credentials and deploy!

---

For detailed information, see:
- `README.md` - Full project overview
- `API_DOCUMENTATION.md` - API reference
- `DEPLOYMENT.md` - Deployment guide
- `PROJECT_SUMMARY.md` - What was built

Good luck! 🎉
