"""Multi-source news scraper - fetches from RSS, NewsAPI, and other free sources"""
import logging
import feedparser
import aiohttp
from typing import List, Dict, Optional
from datetime import datetime
import hashlib
from app.config import settings

logger = logging.getLogger(__name__)


class MultiSourceScraper:
    """Scraper for fetching news from multiple sources"""
    
    # Free RSS feeds (no API key required)
    FREE_RSS_FEEDS = [
        # Tech news
        "https://feeds.techcrunch.com/",
        "https://feeds.arstechnica.com/arstechnica/index",
        "https://feeds.theverge.com/verge/index.xml",
        
        # General news
        "https://feeds.bloomberg.com/markets/news.rss",
        "https://www.cnbc.com/id/100003114/device/rss/rss.html",
        "http://feeds.reuters.com/reuters/businessNews",
        "http://feeds.reuters.com/reuters/technologyNews",
        
        # Business/Finance
        "https://feeds.bloomberg.com/technology/news.rss",
        "http://feeds.reuters.com/reuters/companyNews",
        
        # Science
        "https://feeds.wired.com/feed/rss",
        
        # BBC News
        "http://feeds.bbc.co.uk/news/rss.xml",
        "http://feeds.bbc.co.uk/news/world/rss.xml",
        
        # Guardian
        "https://www.theguardian.com/international/rss",
        "https://www.theguardian.com/technology/rss",
        
        # Hacker News
        "https://news.ycombinator.com/rss",
    ]
    
    def __init__(self):
        self.timeout = aiohttp.ClientTimeout(total=30)
        self.user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    
    async def fetch_from_all_sources(self) -> List[Dict]:
        """Fetch news from all available sources"""
        articles = []
        
        # Fetch from free RSS feeds
        logger.info("Fetching from free RSS feeds...")
        rss_articles = await self._fetch_from_rss_feeds()
        articles.extend(rss_articles)
        logger.info(f"Fetched {len(rss_articles)} articles from RSS feeds")
        
        # Try to fetch from NewsAPI if key is available
        if hasattr(settings, 'NEWSAPI_KEY') and settings.NEWSAPI_KEY:
            logger.info("Fetching from NewsAPI...")
            newsapi_articles = await self._fetch_from_newsapi()
            articles.extend(newsapi_articles)
            logger.info(f"Fetched {len(newsapi_articles)} articles from NewsAPI")
        
        # Try to fetch from Guardian API if key is available
        if hasattr(settings, 'GUARDIAN_API_KEY') and settings.GUARDIAN_API_KEY:
            logger.info("Fetching from Guardian API...")
            guardian_articles = await self._fetch_from_guardian()
            articles.extend(guardian_articles)
            logger.info(f"Fetched {len(guardian_articles)} articles from Guardian")
        
        # Remove duplicates
        articles = self._remove_duplicates(articles)
        logger.info(f"Total unique articles: {len(articles)}")
        
        return articles
    
    async def _fetch_from_rss_feeds(self) -> List[Dict]:
        """Fetch from RSS feeds without API key"""
        articles = []
        
        for feed_url in self.FREE_RSS_FEEDS:
            try:
                feed = feedparser.parse(feed_url)
                
                if feed.bozo and isinstance(feed.bozo_exception, Exception):
                    logger.warning(f"Feed parsing issue for {feed_url}: {feed.bozo_exception}")
                
                for entry in feed.entries[:10]:  # Limit to 10 per feed
                    try:
                        article = {
                            'title': entry.get('title', 'No title'),
                            'description': entry.get('summary', entry.get('description', '')),
                            'url': entry.get('link', ''),
                            'source': feed.feed.get('title', 'Unknown'),
                            'published_at': self._parse_date(entry.get('published', datetime.now().isoformat())),
                            'image_url': self._extract_image(entry),
                            'source_type': 'RSS'
                        }
                        
                        if article['url'] and article['title']:
                            articles.append(article)
                    except Exception as e:
                        logger.warning(f"Error parsing entry from {feed_url}: {str(e)}")
                        continue
                        
            except Exception as e:
                logger.warning(f"Error fetching {feed_url}: {str(e)}")
                continue
        
        return articles
    
    async def _fetch_from_newsapi(self) -> List[Dict]:
        """Fetch from NewsAPI (free tier)"""
        articles = []
        
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                # Fetch top headlines
                url = "https://newsapi.org/v2/top-headlines"
                params = {
                    'country': 'us',
                    'apiKey': settings.NEWSAPI_KEY
                }
                
                async with session.get(url, params=params, headers={'User-Agent': self.user_agent}) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        
                        for article in data.get('articles', [])[:20]:
                            parsed_article = {
                                'title': article.get('title', 'No title'),
                                'description': article.get('description', '') or article.get('content', ''),
                                'url': article.get('url', ''),
                                'source': article.get('source', {}).get('name', 'Unknown'),
                                'published_at': article.get('publishedAt', datetime.now().isoformat()),
                                'image_url': article.get('urlToImage', ''),
                                'source_type': 'NewsAPI'
                            }
                            
                            if parsed_article['url'] and parsed_article['title']:
                                articles.append(parsed_article)
                    else:
                        logger.warning(f"NewsAPI returned status {resp.status}")
                        
        except Exception as e:
            logger.warning(f"Error fetching from NewsAPI: {str(e)}")
        
        return articles
    
    async def _fetch_from_guardian(self) -> List[Dict]:
        """Fetch from Guardian API (free tier)"""
        articles = []
        
        try:
            async with aiohttp.ClientSession(timeout=self.timeout) as session:
                url = "https://open-platform.theguardian.com/search"
                params = {
                    'api-key': settings.GUARDIAN_API_KEY,
                    'page-size': 50,
                    'show-fields': 'thumbnail,trailText'
                }
                
                async with session.get(url, params=params, headers={'User-Agent': self.user_agent}) as resp:
                    if resp.status == 200:
                        data = await resp.json()
                        
                        for result in data.get('response', {}).get('results', [])[:20]:
                            fields = result.get('fields', {})
                            parsed_article = {
                                'title': result.get('webTitle', 'No title'),
                                'description': fields.get('trailText', ''),
                                'url': result.get('webUrl', ''),
                                'source': 'The Guardian',
                                'published_at': result.get('webPublicationDate', datetime.now().isoformat()),
                                'image_url': fields.get('thumbnail', ''),
                                'source_type': 'Guardian'
                            }
                            
                            if parsed_article['url'] and parsed_article['title']:
                                articles.append(parsed_article)
                    else:
                        logger.warning(f"Guardian API returned status {resp.status}")
                        
        except Exception as e:
            logger.warning(f"Error fetching from Guardian: {str(e)}")
        
        return articles
    
    def _parse_date(self, date_str: str) -> str:
        """Parse date string to ISO format"""
        try:
            if isinstance(date_str, str):
                # Try to parse common date formats
                from email.utils import parsedate_to_datetime
                dt = parsedate_to_datetime(date_str)
                return dt.isoformat()
        except Exception:
            pass
        
        return datetime.now().isoformat()
    
    def _extract_image(self, entry: Dict) -> Optional[str]:
        """Extract image URL from RSS entry"""
        try:
            if hasattr(entry, 'media_content') and entry.media_content:
                return entry.media_content[0].get('url', '')
            if 'links' in entry:
                for link in entry.links:
                    if link.get('rel') == 'enclosure' and 'image' in link.get('type', ''):
                        return link.get('href', '')
        except Exception:
            pass
        
        return None
    
    def _remove_duplicates(self, articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles by URL"""
        seen_urls = set()
        unique_articles = []
        
        for article in articles:
            url = article.get('url', '')
            if url and url not in seen_urls:
                seen_urls.add(url)
                unique_articles.append(article)
        
        return unique_articles
