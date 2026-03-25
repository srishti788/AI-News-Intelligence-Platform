from pydantic_settings import BaseSettings
from typing import Optional
import os


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # API Configuration
    API_TITLE: str = "AI News Intelligence Platform"
    API_VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # CORS Configuration
    ALLOWED_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]
    
    # Supabase Configuration
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_JWT_SECRET: str
    
    # OpenAI Configuration
    OPENAI_API_KEY: str
    OPENAI_MODEL: str = "gpt-3.5-turbo"
    
    # Free News APIs (Optional - works without them, but with more sources if provided)
    NEWSAPI_KEY: Optional[str] = None  # Get free key from https://newsapi.org
    GUARDIAN_API_KEY: Optional[str] = None  # Get free key from https://open-platform.theguardian.com
    
    # RSS Feeds
    RSS_FEEDS: list = [
        "https://feeds.bloomberg.com/markets/news.rss",
        "https://feeds.techcrunch.com/",
        "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        "https://feeds.arstechnica.com/arstechnica/index",
        "https://feeds.theverge.com/verge/index.xml"
    ]
    
    # Relay.app Configuration
    RELAY_WEBHOOK_URL: Optional[str] = None
    RELAY_API_KEY: Optional[str] = None
    
    # Email Configuration
    SMTP_SERVER: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USERNAME: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    FROM_EMAIL: Optional[str] = None
    
    # Redis Configuration
    REDIS_URL: Optional[str] = "redis://localhost:6379"
    
    # Scheduling
    SCRAPE_INTERVAL: int = 3600  # 1 hour in seconds
    
    # ML Configuration
    TF_IDF_MAX_FEATURES: int = 5000
    SIMILARITY_THRESHOLD: float = 0.3
    
    # NLTK Data Path
    NLTK_DATA_PATH: str = "./nltk_data"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()
