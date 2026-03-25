"""Data Cleaning and Preprocessing Module"""
import logging
import re
import nltk
from typing import Dict, List, Optional
from html.parser import HTMLParser
from datetime import datetime

logger = logging.getLogger(__name__)


class HTMLCleaner(HTMLParser):
    """HTML parser to extract text"""
    def __init__(self):
        super().__init__()
        self.text = []
    
    def handle_data(self, d):
        self.text.append(d)
    
    def get_text(self):
        return ''.join(self.text)


class DataPreprocessor:
    """Clean and preprocess news articles"""
    
    def __init__(self):
        """Initialize preprocessor"""
        try:
            nltk.download('punkt', quiet=True)
            nltk.download('stopwords', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
        except Exception as e:
            logger.warning(f"Could not download NLTK data: {str(e)}")
    
    @staticmethod
    def clean_html(html_content: str) -> str:
        """Remove HTML tags from content"""
        if not html_content:
            return ""
        
        parser = HTMLCleaner()
        try:
            parser.feed(html_content)
            return parser.get_text()
        except Exception as e:
            logger.error(f"Error cleaning HTML: {str(e)}")
            return html_content
    
    @staticmethod
    def normalize_whitespace(text: str) -> str:
        """Normalize whitespace in text"""
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        # Remove leading/trailing whitespace
        text = text.strip()
        return text
    
    @staticmethod
    def remove_special_characters(text: str, keep_punctuation: bool = True) -> str:
        """Remove special characters from text"""
        if keep_punctuation:
            # Keep alphanumeric, spaces, and basic punctuation
            text = re.sub(r'[^a-zA-Z0-9\s\.\,\!\?\-\:]', '', text)
        else:
            # Keep only alphanumeric and spaces
            text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
        return text
    
    @staticmethod
    def remove_urls(text: str) -> str:
        """Remove URLs from text"""
        url_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        return re.sub(url_pattern, '', text)
    
    @staticmethod
    def remove_email_addresses(text: str) -> str:
        """Remove email addresses from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        return re.sub(email_pattern, '', text)
    
    @staticmethod
    def remove_duplicates(articles: List[Dict]) -> List[Dict]:
        """Remove duplicate articles based on content_hash"""
        seen = set()
        unique_articles = []
        
        for article in articles:
            content_hash = article.get("content_hash")
            if content_hash and content_hash not in seen:
                seen.add(content_hash)
                unique_articles.append(article)
        
        logger.info(f"Removed {len(articles) - len(unique_articles)} duplicates")
        return unique_articles
    
    @staticmethod
    def filter_valid_articles(articles: List[Dict]) -> List[Dict]:
        """Filter out articles with missing critical information"""
        valid_articles = []
        
        for article in articles:
            # Check required fields
            if not article.get("title"):
                logger.warning("Article missing title, skipping")
                continue
            if not article.get("url"):
                logger.warning(f"Article '{article.get('title')}' missing URL, skipping")
                continue
            if not article.get("content") or len(article.get("content", "").strip()) < 10:
                logger.warning(f"Article '{article.get('title')}' has insufficient content, skipping")
                continue
            
            valid_articles.append(article)
        
        return valid_articles
    
    def preprocess_article(self, article: Dict) -> Dict:
        """Complete preprocessing pipeline for an article"""
        try:
            # Clean content
            content = article.get("content", "")
            content = self.clean_html(content)
            content = self.remove_urls(content)
            content = self.remove_email_addresses(content)
            content = self.normalize_whitespace(content)
            
            # Clean title
            title = article.get("title", "")
            title = self.normalize_whitespace(title)
            
            # Update article with cleaned content
            article["content"] = content
            article["title"] = title
            article["processed_at"] = datetime.utcnow().isoformat()
            
            return article
        except Exception as e:
            logger.error(f"Error preprocessing article: {str(e)}")
            return article
    
    def batch_preprocess(self, articles: List[Dict]) -> List[Dict]:
        """Preprocess multiple articles"""
        logger.info(f"Starting preprocessing of {len(articles)} articles")
        
        # Remove duplicates
        articles = self.remove_duplicates(articles)
        
        # Filter valid articles
        articles = self.filter_valid_articles(articles)
        
        # Preprocess each article
        processed_articles = []
        for article in articles:
            processed = self.preprocess_article(article)
            processed_articles.append(processed)
        
        logger.info(f"Completed preprocessing of {len(processed_articles)} articles")
        return processed_articles


class TextExtractor:
    """Extract key information from text"""
    
    @staticmethod
    def extract_sentences(text: str, limit: int = 5) -> List[str]:
        """Extract first N sentences from text"""
        try:
            sentences = nltk.sent_tokenize(text)
            return sentences[:limit]
        except Exception as e:
            logger.error(f"Error extracting sentences: {str(e)}")
            # Fallback: split by period
            sentences = [s.strip() for s in text.split('.') if s.strip()]
            return sentences[:limit]
    
    @staticmethod
    def extract_keywords(text: str, limit: int = 10) -> List[str]:
        """Extract keywords from text"""
        try:
            from nltk.corpus import stopwords
            stop_words = set(stopwords.words('english'))
            
            # Tokenize and clean
            words = nltk.word_tokenize(text.lower())
            keywords = [
                word for word in words
                if word.isalnum() and word not in stop_words and len(word) > 2
            ]
            
            # Get unique keywords preserving order
            seen = set()
            unique_keywords = []
            for keyword in keywords:
                if keyword not in seen:
                    seen.add(keyword)
                    unique_keywords.append(keyword)
            
            return unique_keywords[:limit]
        except Exception as e:
            logger.error(f"Error extracting keywords: {str(e)}")
            return []
