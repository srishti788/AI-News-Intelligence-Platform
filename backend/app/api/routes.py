"""FastAPI Routes for News Intelligence Platform"""
import logging
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime
from app.database.supabase_client import db
from app.scrapers.multi_source_scraper import MultiSourceScraper
from app.utils.data_preprocessor import DataPreprocessor
from app.ai_processing.ai_processor import AIProcessor
from app.ml_engine.recommendation_engine import RecommendationEngine
from app.email_service.relay_service import RelayEmailService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1", tags=["news"])

# Models
class ArticleInput(BaseModel):
    title: str
    content: str
    url: str
    source: str

class SummaryRequest(BaseModel):
    article_id: str
    style: str = "bullet"

class RecommendationRequest(BaseModel):
    user_id: str
    limit: int = 10

class ChatRequest(BaseModel):
    question: str
    user_id: Optional[str] = None

class UserPreferences(BaseModel):
    user_id: str
    interests: List[str]
    categories: List[str]
    sentiment_filter: Optional[str] = None

# Dependencies
async def get_ai_processor() -> AIProcessor:
    return AIProcessor()

async def get_recommendation_engine() -> RecommendationEngine:
    return RecommendationEngine()

# =================== NEWS ENDPOINTS ===================

@router.post("/scrape")
async def scrape_rss_feeds():
    """Scrape news from multiple free sources (RSS, NewsAPI, Guardian)"""
    try:
        # Use multi-source scraper instead of single RSS scraper
        scraper = MultiSourceScraper()
        articles = await scraper.fetch_from_all_sources()
        
        logger.info(f"Fetched {len(articles)} articles from multiple sources")
        
        preprocessor = DataPreprocessor()
        articles = preprocessor.batch_preprocess(articles)
        
        # Store articles in database
        stored_count = 0
        for article in articles:
            try:
                await db.insert_article(article)
                stored_count += 1
            except Exception as e:
                logger.warning(f"Error storing article: {str(e)}")
                continue
        
        return {
            "status": "success",
            "articles_scraped": len(articles),
            "articles_stored": stored_count,
            "sources": ["RSS Feeds", "NewsAPI", "Guardian API"],
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Error scraping feeds: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/test-scrape")
async def test_scrape():
    """Test endpoint - returns raw scraped articles without storing"""
    try:
        scraper = MultiSourceScraper()
        articles = await scraper.fetch_from_all_sources()
        
        logger.info(f"Test: Fetched {len(articles)} articles")
        
        return {
            "status": "success",
            "articles_count": len(articles),
            "sample_articles": articles[:3],  # Return first 3 as sample
            "sources": ["RSS Feeds", "NewsAPI", "Guardian API"]
        }
    except Exception as e:
        logger.error(f"Error in test scrape: {str(e)}")
        return {
            "status": "error",
            "error": str(e)
        }

@router.get("/articles")
async def get_articles(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    category: Optional[str] = None,
    sentiment: Optional[str] = None
):
    """Get articles with optional filtering"""
    try:
        articles = await db.get_articles(limit=limit, offset=skip)
        
        # If no articles in DB, return mock data for now
        if not articles or len(articles) == 0:
            logger.warning("No articles in database, returning mock data")
            articles = get_mock_articles()[skip:skip+limit]
        
        # Filter by category if provided
        if category:
            articles = [a for a in articles if a.get("category") == category]
        
        # Filter by sentiment if provided
        if sentiment:
            articles = [a for a in articles if a.get("sentiment") == sentiment]
        
        return {
            "status": "success",
            "count": len(articles),
            "articles": articles
        }
    except Exception as e:
        logger.error(f"Error fetching articles: {str(e)}")
        # Return mock data on error
        logger.warning("Returning mock data due to error")
        mock = get_mock_articles()[skip:skip+limit]
        return {
            "status": "success",
            "count": len(mock),
            "articles": mock,
            "note": "Using mock data - database connection error"
        }

def get_mock_articles():
    """Return mock articles for testing"""
    return [
        {
            "id": "1",
            "title": "Tech Giants Release New AI Models with Enhanced Capabilities",
            "content": "Leading technology companies have announced breakthrough developments in artificial intelligence, introducing models with significantly improved performance and efficiency. The new systems promise to revolutionize various industries.",
            "description": "Major tech companies unveil next-generation AI models with enhanced capabilities",
            "category": "technology",
            "sentiment": "positive",
            "source": "Tech News Today",
            "image_url": "https://via.placeholder.com/500x300?text=AI+Models",
            "url": "https://example.com/ai-models",
            "published_at": "2026-03-25T10:00:00Z"
        },
        {
            "id": "2",
            "title": "Global Markets Experience Volatility Amid Economic Shifts",
            "content": "Financial markets around the world have shown mixed signals as investors grapple with changing economic conditions. The volatility reflects ongoing uncertainty about interest rates and inflation trends.",
            "description": "Stock markets fluctuate as economic indicators send mixed signals",
            "category": "finance",
            "sentiment": "neutral",
            "source": "Bloomberg Markets",
            "image_url": "https://via.placeholder.com/500x300?text=Markets",
            "url": "https://example.com/markets",
            "published_at": "2026-03-25T09:30:00Z"
        },
        {
            "id": "3",
            "title": "Renewable Energy Adoption Reaches Record Highs",
            "content": "Countries and organizations worldwide have accelerated their transition to renewable energy sources, setting new records for both installations and efficiency. This shift is expected to significantly reduce global carbon emissions.",
            "description": "Renewable energy sources hit unprecedented adoption milestones globally",
            "category": "environment",
            "sentiment": "positive",
            "source": "Green Energy Report",
            "image_url": "https://via.placeholder.com/500x300?text=Renewable+Energy",
            "url": "https://example.com/renewable-energy",
            "published_at": "2026-03-25T08:45:00Z"
        },
        {
            "id": "4",
            "title": "New Startup Secures Record-Breaking Funding Round",
            "content": "An innovative startup has attracted unprecedented investment from leading venture capital firms, signaling strong confidence in its revolutionary technology and business model. The funding will accelerate development and market expansion.",
            "description": "Emerging company raises historic investment amount for growth",
            "category": "business",
            "sentiment": "positive",
            "source": "Startup News",
            "image_url": "https://via.placeholder.com/500x300?text=Startup+Funding",
            "url": "https://example.com/startup-funding",
            "published_at": "2026-03-25T07:20:00Z"
        },
        {
            "id": "5",
            "title": "Scientists Discover Promising Treatment for Common Disease",
            "content": "Medical researchers have announced a significant breakthrough in treating a widespread health condition. Initial trials show remarkable results, offering hope to millions of patients worldwide seeking more effective treatments.",
            "description": "Researchers unveil breakthrough medical treatment with promising results",
            "category": "health",
            "sentiment": "positive",
            "source": "Medical Today",
            "image_url": "https://via.placeholder.com/500x300?text=Medical+Breakthrough",
            "url": "https://example.com/medical-treatment",
            "published_at": "2026-03-25T06:15:00Z"
        },
    ]

@router.get("/articles/{article_id}")
async def get_article_detail(article_id: str):
    """Get detailed information about a specific article"""
    try:
        article = await db.get_article_by_id(article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        # Get summary
        summary = await db.get_summary_by_article_id(article_id)
        
        return {
            "status": "success",
            "article": article,
            "summary": summary
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching article detail: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search")
async def search_articles(
    query: str = Query(..., min_length=1),
    limit: int = Query(50, ge=1, le=100)
):
    """Search articles by title or content"""
    try:
        articles = await db.search_articles(query, limit=limit)
        return {
            "status": "success",
            "query": query,
            "count": len(articles),
            "articles": articles
        }
    except Exception as e:
        logger.error(f"Error searching articles: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# =================== AI PROCESSING ENDPOINTS ===================

@router.post("/summary")
async def get_article_summary(
    request: SummaryRequest,
    ai_processor: AIProcessor = Depends(get_ai_processor)
):
    """Generate AI summary for an article"""
    try:
        article = await db.get_article_by_id(request.article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        summary = await ai_processor.summarize_article(
            title=article.get("title", ""),
            content=article.get("content", ""),
            style=request.style
        )
        
        # Store summary in database
        summary_data = {
            "article_id": request.article_id,
            "summary": summary.get("summary"),
            "style": request.style,
            "created_at": datetime.utcnow().isoformat()
        }
        stored_summary = await db.insert_summary(summary_data)
        
        return {
            "status": "success",
            "article_id": request.article_id,
            "summary": summary.get("summary"),
            "model": summary.get("model")
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error generating summary: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/analyze")
async def analyze_article(
    article_id: str = Query(...),
    ai_processor: AIProcessor = Depends(get_ai_processor)
):
    """Comprehensive analysis of an article"""
    try:
        article = await db.get_article_by_id(article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        content = article.get("content", "")
        
        # Get sentiment
        sentiment = await ai_processor.analyze_sentiment(content)
        
        # Extract keywords
        keywords = await ai_processor.extract_keywords(content)
        
        return {
            "status": "success",
            "article_id": article_id,
            "sentiment": sentiment,
            "keywords": keywords,
            "title": article.get("title")
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error analyzing article: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat")
async def chat_with_ai(
    request: ChatRequest,
    ai_processor: AIProcessor = Depends(get_ai_processor)
):
    """Chat with AI about news - searches for relevant articles and returns them"""
    try:
        # Search for articles matching the user's question/topic
        articles = await db.search_articles(request.question, limit=10)
        
        if not articles:
            # Fallback to recent articles if no search results
            articles = await db.get_articles(limit=5)
        
        # Get AI response/answer
        response = await ai_processor.answer_question(
            question=request.question,
            context=articles if articles else [{
                "title": "General Knowledge",
                "content": "Latest news information"
            }]
        )
        
        # Log activity if user_id provided
        if request.user_id:
            try:
                await db.log_activity(
                    request.user_id,
                    {
                        "action": "chat",
                        "metadata": {"question": request.question, "articles_found": len(articles)}
                    }
                )
            except Exception as e:
                logger.warning(f"Could not log activity: {str(e)}")
        
        return {
            "status": "success",
            "question": request.question,
            "answer": response.get("answer", ""),
            "articles": articles,  # Return the relevant articles
            "num_articles": len(articles),
            "topic": request.question,  # Topic that can be used to update the feed
            "source": response.get("source", "Unknown")
        }
    except Exception as e:
        logger.error(f"Error in chat: {str(e)}")
        # Return a graceful fallback instead of error
        return {
            "status": "error",
            "question": request.question,
            "answer": f"I encountered an error processing your question: {str(e)}. Please try again or rephrase your question.",
            "articles": [],
            "num_articles": 0,
            "topic": request.question
        }

# =================== RECOMMENDATION ENDPOINTS ===================

@router.post("/recommendations")
async def get_recommendations(
    request: RecommendationRequest
):
    """Get personalized recommendations"""
    try:
        # Get user preferences
        preferences = await db.get_user_preferences(request.user_id)
        
        if not preferences:
            # Return trending articles if no preferences
            rec_engine = RecommendationEngine()
            articles = await db.get_articles(limit=request.limit)
            if articles:
                rec_engine.fit(articles)
                recommendations = rec_engine.get_trending_articles(top_k=request.limit)
            else:
                recommendations = []
        else:
            rec_engine = RecommendationEngine()
            articles = await db.get_articles(limit=1000)
            
            if articles:
                rec_engine.fit(articles)
                recommendations = rec_engine.get_personalized_recommendations(
                    user_preferences=preferences,
                    top_k=request.limit
                )
            else:
                recommendations = []
        
        return {
            "status": "success",
            "user_id": request.user_id,
            "count": len(recommendations),
            "recommendations": recommendations
        }
    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/similar/{article_id}")
async def get_similar_articles(
    article_id: str,
    limit: int = Query(5, ge=1, le=20)
):
    """Get articles similar to a given article"""
    try:
        # Get article
        article = await db.get_article_by_id(article_id)
        if not article:
            raise HTTPException(status_code=404, detail="Article not found")
        
        # Get all articles for similarity calculation
        all_articles = await db.get_articles(limit=1000)
        
        rec_engine = RecommendationEngine()
        if all_articles:
            rec_engine.fit(all_articles)
            similar = rec_engine.get_similar_articles(article_id, top_k=limit)
        else:
            similar = []
        
        return {
            "status": "success",
            "article_id": article_id,
            "count": len(similar),
            "similar_articles": similar
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting similar articles: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# =================== USER PREFERENCE ENDPOINTS ===================

@router.post("/preferences")
async def set_user_preferences(preferences: UserPreferences):
    """Set user preferences"""
    try:
        result = await db.set_user_preferences(
            preferences.user_id,
            preferences.dict()
        )
        return {
            "status": "success",
            "user_id": preferences.user_id,
            "preferences": result
        }
    except Exception as e:
        logger.error(f"Error setting preferences: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/preferences/{user_id}")
async def get_user_preferences(user_id: str):
    """Get user preferences"""
    try:
        preferences = await db.get_user_preferences(user_id)
        if not preferences:
            raise HTTPException(status_code=404, detail="Preferences not found")
        
        return {
            "status": "success",
            "user_id": user_id,
            "preferences": preferences
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching preferences: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

# =================== HEALTH CHECK ===================

@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "News Intelligence Platform API"
    }
