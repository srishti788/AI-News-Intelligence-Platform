"""RSS Feed Scraper Module"""
import logging
import feedparser
import aiohttp
from typing import List, Dict, Optional
from datetime import datetime
import hashlib
from urllib.parse import urlparse

logger = logging.getLogger(__name__)


class RSSScraperConfig:
    """Configuration for RSS scraper"""
    TIMEOUT = 30
    USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"


class RSSScraper:
    """Scraper for fetching and parsing RSS feeds"""
    
    def __init__(self, feeds: List[str]):
        """Initialize scraper with feed URLs"""
        self.feeds = feeds
        self.parsed_articles = []
    
    async def fetch_all_feeds(self) -> List[Dict]:
        """Fetch and parse all RSS feeds"""
        articles = []
        
        for feed_url in self.feeds:
            try:
                feed_articles = await self.fetch_feed(feed_url)
                articles.extend(feed_articles)
            except Exception as e:
                logger.warning(f"Error fetching {feed_url}: {str(e)}")
                continue
        
        return articles
    
    async def fetch_feed(self, feed_url: str) -> List[Dict]:
        """Fetch and parse a single RSS feed"""
        try:
            # Parse feed using feedparser
            feed = feedparser.parse(feed_url)
            
            if feed.bozo and isinstance(feed.bozo_exception, Exception):
                logger.warning(f"Feed parsing issue for {feed_url}: {feed.bozo_exception}")
            
            articles = []
            source_name = feed.feed.get("title", urlparse(feed_url).netloc)
            
            for entry in feed.entries:
                try:
                    article = self._parse_entry(entry, feed_url, source_name)
                    if article:
                        articles.append(article)
                except Exception as e:
                    logger.error(f"Error parsing entry: {str(e)}")
                    continue
            
            logger.info(f"Fetched {len(articles)} articles from {source_name}")
            return articles
            
        except Exception as e:
            logger.error(f"Error fetching feed {feed_url}: {str(e)}")
            raise
    
    def _parse_entry(self, entry: dict, feed_url: str, source_name: str) -> Optional[Dict]:
        """Parse a single RSS entry"""
        try:
            title = entry.get("title", "No Title")
            link = entry.get("link", "")
            description = entry.get("summary", "")
            
            # Parse publish date
            published = None
            if entry.get("published_parsed"):
                published = datetime(*entry.published_parsed[:6])
            elif entry.get("updated_parsed"):
                published = datetime(*entry.updated_parsed[:6])
            else:
                published = datetime.utcnow()
            
            # Generate unique ID
            content = f"{title}{link}{published.isoformat()}"
            unique_id = hashlib.md5(content.encode()).hexdigest()
            
            # Extract author
            author = "Unknown"
            if entry.get("author"):
                author = entry.author
            elif entry.get("author_detail"):
                author = entry.author_detail.get("name", "Unknown")
            
            return {
                "id": unique_id,
                "title": title,
                "content": description,
                "url": link,
                "source": source_name,
                "source_url": feed_url,
                "author": author,
                "published_at": published.isoformat(),
                "scraped_at": datetime.utcnow().isoformat(),
                "category": self._extract_category(entry),
                "image_url": self._extract_image(entry),
                "content_hash": unique_id
            }
        except Exception as e:
            logger.error(f"Error parsing entry details: {str(e)}")
            return None
    
    def _extract_category(self, entry: dict) -> str:
        """Extract category from RSS entry"""
        if entry.get("tags"):
            return entry.tags[0].get("term", "General")
        if entry.get("category"):
            return entry.category
        return "General"
    
    def _extract_image(self, entry: dict) -> Optional[str]:
        """Extract image URL from RSS entry"""
        if entry.get("media_content"):
            return entry.media_content[0].get("url")
        if entry.get("image"):
            return entry.image.get("href")
        return None


class FeedValidator:
    """Validate RSS feeds"""
    
    @staticmethod
    def is_valid_feed(feed_url: str) -> bool:
        """Check if URL is a valid RSS feed"""
        try:
            feed = feedparser.parse(feed_url)
            return len(feed.entries) > 0
        except Exception as e:
            logger.error(f"Feed validation error: {str(e)}")
            return False
    
    @staticmethod
    def get_feed_info(feed_url: str) -> Optional[Dict]:
        """Get metadata about a feed"""
        try:
            feed = feedparser.parse(feed_url)
            return {
                "title": feed.feed.get("title", "Unknown"),
                "description": feed.feed.get("description", ""),
                "link": feed.feed.get("link", ""),
                "entry_count": len(feed.entries),
                "last_updated": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Error getting feed info: {str(e)}")
            return None
