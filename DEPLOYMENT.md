# Deployment Guide

This guide covers deploying the News Intelligence Platform to production using Render, Vercel, and Supabase Cloud.

## 📋 Prerequisites

Before deployment, ensure you have:
1. GitHub account with the repository
2. Render account (https://render.com)
3. Vercel account (https://vercel.com) - for frontend
4. Supabase account (https://supabase.com)
5. OpenAI API key
6. Relay.app webhook URL (optional)

## 🗄️ Step 1: Database Setup (Supabase)

### 1.1 Create Supabase Project
1. Go to https://supabase.com
2. Create new project
3. Note your project URL and API keys

### 1.2 Setup Database Tables
1. Go to SQL Editor in Supabase dashboard
2. Paste the contents of `backend/database_schema.sql`
3. Run the SQL

### 1.3 Configure Authentication
1. Go to Authentication settings
2. Enable Email provider
3. Set redirect URLs:
   ```
   http://localhost:3000/auth/callback
   https://your-frontend-url/auth/callback
   ```

### 1.4 Get Credentials
In Settings → API:
- Copy Project URL
- Copy anon/public key
- Copy service_role key (for backend)

## 🔧 Step 2: Backend Deployment (Render)

### 2.1 Prepare Repository
Create a `.render.yaml` in backend root:
```yaml
services:
  - type: web
    name: news-intelligence-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port 8000
    envVars:
      - key: DEBUG
        value: false
      - key: PYTHON_VERSION
        value: 3.11
```

### 2.2 Deploy on Render
1. Go to https://render.com
2. Click "New +" → "Web Service"
3. Connect GitHub repository
4. Select backend directory
5. Configure:
   - **Name**: `news-intelligence-api`
   - **Environment**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port 8000`
   - **Instance Type**: Starter (or higher for production)

### 2.3 Set Environment Variables
In Render dashboard, go to Environment:
```env
DEBUG=false
HOST=0.0.0.0
PORT=8000
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
SUPABASE_JWT_SECRET=your_jwt_secret
OPENAI_API_KEY=sk-your-key
OPENAI_MODEL=gpt-3.5-turbo
RELAY_WEBHOOK_URL=your_relay_webhook
RELAY_API_KEY=your_relay_key
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
FROM_EMAIL=your_email@gmail.com
REDIS_URL=redis://your-redis-url
TF_IDF_MAX_FEATURES=5000
SIMILARITY_THRESHOLD=0.3
```

### 2.4 Deploy
- Click "Create Web Service"
- Monitor build in Logs tab
- Service will be available at: `https://news-intelligence-api.onrender.com`

## 🎨 Step 3: Frontend Deployment

### Option A: Deploy on Vercel

#### 3A.1 Prepare Files
Create `vercel.json` in frontend root:
```json
{
  "buildCommand": "npm install && npm run build",
  "outputDirectory": "dist",
  "env": {
    "VITE_SUPABASE_URL": "@supabase_url",
    "VITE_SUPABASE_ANON_KEY": "@supabase_anon_key",
    "VITE_API_BASE_URL": "@api_base_url"
  }
}
```

#### 3A.2 Deploy
1. Go to https://vercel.com
2. Click "Add New" → "Project"
3. Import GitHub repository
4. Select frontend directory
5. Configure project settings
6. Add environment variables
7. Click "Deploy"

### Option B: Deploy on Render

#### 3B.1 Configure
1. Go to Render dashboard
2. Click "New +" → "Static Site"
3. Connect GitHub repository
4. Select frontend directory
5. Configure:
   - **Build Command**: `npm install && npm run build`
   - **Publish Directory**: `dist`

#### 3B.2 Set Environment Variables
```env
VITE_SUPABASE_URL=your_supabase_url
VITE_SUPABASE_ANON_KEY=your_anon_key
VITE_API_BASE_URL=https://news-intelligence-api.onrender.com/api/v1
```

#### 3B.3 Deploy
- Click "Create Static Site"
- Deployment will start automatically
- Site URL provided after completion

## 📧 Step 4: Setup Email Service (Relay.app)

### 4.1 Create Relay Account
1. Go to https://relay.app
2. Sign up and create account
3. Create webhook endpoint

### 4.2 Configure Webhook
1. In Relay dashboard, go to Webhooks
2. Create new webhook
3. Set endpoint URL: `https://your-backend-url/api/v1/email/send`
4. Copy webhook URL and secret

### 4.3 Update Backend
Add webhook credentials to Render environment variables

## 🔐 Step 5: Security Configuration

### 5.1 Enable HTTPS
- Both Render and Vercel provide free HTTPS
- Ensure certificate is valid

### 5.2 Configure CORS
Update backend `config.py`:
```python
ALLOWED_ORIGINS = [
    "https://your-frontend-url.vercel.app",
    "https://your-frontend-url.onrender.com",
    "http://localhost:3000"
]
```

### 5.3 Set up Authentication
1. Configure Supabase redirects
2. Update frontend API base URL
3. Test login flow

### 5.4 Secure Secrets
- Use environment variables for all secrets
- Enable "Expose as secret" in Render for sensitive values
- Rotate API keys regularly

## 📊 Step 6: Monitoring & Logging

### 6.1 Backend Monitoring
1. Render provides logs in dashboard
2. Monitor resource usage
3. Set up alerts (if available in plan)

### 6.2 Frontend Monitoring
1. Vercel/Render shows deployment logs
2. Monitor build performance
3. Check error rates

### 6.3 Database Monitoring
1. Supabase has analytics dashboard
2. Monitor query performance
3. Check storage usage

## 🚀 Step 7: Production Checklist

- [ ] Database tables created and seeded
- [ ] Backend deployed and accessible
- [ ] Frontend deployed and loads correctly
- [ ] API endpoints responding to requests
- [ ] Authentication working end-to-end
- [ ] Email service configured
- [ ] Environment variables set correctly
- [ ] HTTPS enabled
- [ ] CORS properly configured
- [ ] Error logging enabled
- [ ] Performance monitoring active
- [ ] Backups configured in Supabase
- [ ] SSL certificates valid
- [ ] DNS records pointing to services
- [ ] Documentation updated

## 🧪 Step 8: Testing Deployment

### 8.1 API Testing
```bash
# Health check
curl https://your-backend-url/api/v1/health

# Get articles
curl https://your-backend-url/api/v1/articles?limit=5

# Chat
curl -X POST https://your-backend-url/api/v1/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "Test"}'
```

### 8.2 Frontend Testing
1. Open frontend URL in browser
2. Check console for errors
3. Test authentication flow
4. Test main features:
   - Search functionality
   - News feed loading
   - AI chat
   - Recommendations

### 8.3 Email Testing
```bash
# Send test email
curl -X POST https://your-backend-url/api/v1/email/send \
  -H "Content-Type: application/json" \
  -d '{
    "to": "test@example.com",
    "subject": "Test Email",
    "body": "Test message"
  }'
```

## 📈 Step 9: Performance Optimization

### Backend
1. Enable caching with Redis
2. Optimize database queries
3. Use object reuse
4. Implement rate limiting

### Frontend
1. Code splitting
2. Lazy loading
3. Image optimization
4. Bundle size analysis

### Database
1. Create appropriate indices
2. Optimize queries
3. Archive old data
4. Monitor slow queries

## 🔄 Step 10: CI/CD Pipeline (Optional)

### GitHub Actions Example
Create `.github/workflows/deploy.yml`:
```yaml
name: Deploy

on:
  push:
    branches: [ main ]

jobs:
  deploy-backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Render
        run: |
          curl -X POST https://api.render.com/deploy/srv-${{ secrets.RENDER_SERVICE_ID }}?key=${{ secrets.RENDER_API_KEY }}

  deploy-frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        run: |
          npx vercel --prod --token ${{ secrets.VERCEL_TOKEN }}
```

## 🆘 Troubleshooting

### Backend Won't Start
1. Check logs in Render dashboard
2. Verify environment variables
3. Test locally first

### Frontend Not Loading
1. Check build logs
2. Verify API base URL
3. Check console for errors

### API Not Responding
1. Check backend service status
2. Verify network connectivity
3. Check CORS configuration

### Database Connection Failed
1. Verify Supabase credentials
2. Check network rules
3. Ensure tables exist

### Email Not Sending
1. Verify Relay.app credentials
2. Check webhook URL
3. Test SMTP fallback

## 📱 Post-Deployment Steps

1. **Monitor Performance**
   - Watch logs for errors
   - Monitor resource usage
   - Track API response times

2. **Gather Feedback**
   - Get user feedback
   - Monitor analytics
   - Note improvement areas

3. **Regular Maintenance**
   - Update dependencies
   - Rotate secrets monthly
   - Review logs weekly
   - Optimize slow queries

4. **Scale When Needed**
   - Upgrade Render plan if needed
   - Implement caching
   - Optimize database
   - Add CDN for frontend

## 📞 Support

For Render issues: https://render.com/docs
For Vercel issues: https://vercel.com/docs
For Supabase issues: https://supabase.com/docs

---

**Deployment Complete!** Your News Intelligence Platform is now live.
