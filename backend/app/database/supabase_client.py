"""Database module for Supabase integration"""
import logging
from typing import Optional, List, Dict, Any
from supabase import create_client, Client
from app.config import settings
from datetime import datetime

logger = logging.getLogger(__name__)


class SupabaseDB:
    """Singleton class for Supabase database operations"""
    
    _instance: Optional['SupabaseDB'] = None
    _client: Optional[Client] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseDB, cls).__new__(cls)
            cls._instance._initialize()
        return cls._instance
    
    def _initialize(self):
        """Initialize Supabase client"""
        try:
            self._client = create_client(
                settings.SUPABASE_URL,
                settings.SUPABASE_KEY
            )
            logger.info("Supabase client initialized successfully")
        except Exception as e:
            logger.warning(f"Failed to initialize Supabase client: {str(e)}")
            logger.info("Supabase client will be in mock mode")
            # Don't raise - allow the app to continue in development mode
    
    @property
    def client(self) -> Client:
        """Get Supabase client"""
        if self._client is None:
            self._initialize()
        return self._client
    
    # =================== ARTICLE OPERATIONS ===================
    
    async def insert_article(self, article: Dict[str, Any]) -> Dict[str, Any]:
        """Insert a new article"""
        try:
            response = self.client.table("articles").insert(article).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error inserting article: {str(e)}")
            raise
    
    async def get_articles(self, limit: int = 50, offset: int = 0) -> List[Dict]:
        """Get articles with pagination"""
        try:
            response = (
                self.client.table("articles")
                .select("*")
                .order("published_at", desc=True)
                .range(offset, offset + limit - 1)
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching articles: {str(e)}")
            raise
    
    async def get_article_by_id(self, article_id: str) -> Optional[Dict]:
        """Get article by ID"""
        try:
            response = (
                self.client.table("articles")
                .select("*")
                .eq("id", article_id)
                .single()
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching article: {str(e)}")
            return None
    
    async def search_articles(self, query: str, limit: int = 50) -> List[Dict]:
        """Search articles by title or content"""
        try:
            response = (
                self.client.table("articles")
                .select("*")
                .ilike("title", f"%{query}%")
                .limit(limit)
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error searching articles: {str(e)}")
            raise
    
    # =================== SUMMARY OPERATIONS ===================
    
    async def insert_summary(self, summary: Dict[str, Any]) -> Dict[str, Any]:
        """Insert article summary"""
        try:
            response = self.client.table("summaries").insert(summary).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error inserting summary: {str(e)}")
            raise
    
    async def get_summary_by_article_id(self, article_id: str) -> Optional[Dict]:
        """Get summary for an article"""
        try:
            response = (
                self.client.table("summaries")
                .select("*")
                .eq("article_id", article_id)
                .single()
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching summary: {str(e)}")
            return None
    
    # =================== USER OPERATIONS ===================
    
    async def create_user(self, user: Dict[str, Any]) -> Dict[str, Any]:
        """Create new user"""
        try:
            response = self.client.table("users").insert(user).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error creating user: {str(e)}")
            raise
    
    async def get_user(self, user_id: str) -> Optional[Dict]:
        """Get user by ID"""
        try:
            response = (
                self.client.table("users")
                .select("*")
                .eq("id", user_id)
                .single()
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching user: {str(e)}")
            return None
    
    async def update_user(self, user_id: str, updates: Dict[str, Any]) -> Optional[Dict]:
        """Update user information"""
        try:
            response = (
                self.client.table("users")
                .update(updates)
                .eq("id", user_id)
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error updating user: {str(e)}")
            raise
    
    # =================== USER PREFERENCES ===================
    
    async def set_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> Dict:
        """Set or update user preferences"""
        try:
            preference_data = {
                "user_id": user_id,
                "interests": preferences.get("interests", []),
                "sentiment_filter": preferences.get("sentiment_filter"),
                "categories": preferences.get("categories", []),
                "updated_at": datetime.utcnow().isoformat()
            }
            response = (
                self.client.table("user_preferences")
                .upsert(preference_data, on_conflict="user_id")
                .execute()
            )
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error setting preferences: {str(e)}")
            raise
    
    async def get_user_preferences(self, user_id: str) -> Optional[Dict]:
        """Get user preferences"""
        try:
            response = (
                self.client.table("user_preferences")
                .select("*")
                .eq("user_id", user_id)
                .single()
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching preferences: {str(e)}")
            return None
    
    # =================== USER ACTIVITY ===================
    
    async def log_activity(self, user_id: str, activity: Dict[str, Any]) -> Dict:
        """Log user activity"""
        try:
            activity_data = {
                "user_id": user_id,
                "action": activity.get("action"),
                "article_id": activity.get("article_id"),
                "metadata": activity.get("metadata", {}),
                "created_at": datetime.utcnow().isoformat()
            }
            response = self.client.table("user_activity").insert(activity_data).execute()
            return response.data[0] if response.data else None
        except Exception as e:
            logger.error(f"Error logging activity: {str(e)}")
            raise
    
    async def get_user_activity(self, user_id: str, limit: int = 50) -> List[Dict]:
        """Get user activity history"""
        try:
            response = (
                self.client.table("user_activity")
                .select("*")
                .eq("user_id", user_id)
                .order("created_at", desc=True)
                .limit(limit)
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching user activity: {str(e)}")
            raise


# Create singleton instance
db = SupabaseDB()
