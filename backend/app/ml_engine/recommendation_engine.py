"""Machine Learning Engine for TF-IDF and Recommendations"""
import logging
import numpy as np
from typing import List, Dict, Optional, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from app.config import settings
import pickle
import os
from datetime import datetime

logger = logging.getLogger(__name__)


class RecommendationEngine:
    """ML-powered recommendation engine using TF-IDF and cosine similarity"""
    
    def __init__(self, max_features: int = None):
        """Initialize the recommendation engine"""
        self.max_features = max_features or settings.TF_IDF_MAX_FEATURES
        self.similarity_threshold = settings.SIMILARITY_THRESHOLD
        self.vectorizer = TfidfVectorizer(
            max_features=self.max_features,
            stop_words='english',
            min_df=1,
            max_df=0.9,
            ngram_range=(1, 2)
        )
        self.tfidf_matrix = None
        self.articles = []
        self.is_fitted = False
        self.model_cache_path = "./models/tfidf_model.pkl"
    
    def fit(self, articles: List[Dict]) -> None:
        """Train TF-IDF vectorizer on articles"""
        try:
            if not articles:
                logger.warning("No articles provided for fitting")
                return
            
            # Extract text from articles
            texts = [
                f"{article.get('title', '')} {article.get('content', '')}"
                for article in articles
            ]
            
            # Fit and transform
            self.tfidf_matrix = self.vectorizer.fit_transform(texts)
            self.articles = articles
            self.is_fitted = True
            
            logger.info(f"TF-IDF model fitted with {len(articles)} articles")
            self._save_model()
        except Exception as e:
            logger.error(f"Error fitting TF-IDF model: {str(e)}")
            raise
    
    def get_similar_articles(self, article_id: str, top_k: int = 5) -> List[Dict]:
        """Get similar articles to a given article"""
        try:
            if not self.is_fitted:
                logger.warning("Model not fitted. Cannot get recommendations.")
                return []
            
            # Find article index
            article_index = None
            for idx, article in enumerate(self.articles):
                if article.get("id") == article_id:
                    article_index = idx
                    break
            
            if article_index is None:
                logger.warning(f"Article {article_id} not found")
                return []
            
            # Calculate similarity scores
            similarity_scores = cosine_similarity(
                self.tfidf_matrix[article_index],
                self.tfidf_matrix
            )[0]
            
            # Get top similar articles (excluding self)
            similar_indices = np.argsort(similarity_scores)[::-1]
            
            results = []
            for idx in similar_indices:
                if idx == article_index:
                    continue  # Skip self
                
                score = float(similarity_scores[idx])
                
                if score >= self.similarity_threshold:
                    article = self.articles[idx]
                    article_copy = article.copy()
                    article_copy["similarity_score"] = round(score, 3)
                    results.append(article_copy)
                
                if len(results) >= top_k:
                    break
            
            logger.info(f"Found {len(results)} similar articles for {article_id}")
            return results
        except Exception as e:
            logger.error(f"Error getting similar articles: {str(e)}")
            return []
    
    def get_personalized_recommendations(
        self,
        user_preferences: Dict,
        top_k: int = 10
    ) -> List[Dict]:
        """Get personalized recommendations based on user preferences"""
        try:
            if not self.is_fitted or not self.articles:
                return []
            
            # Extract user interests
            interests = user_preferences.get("interests", [])
            categories = user_preferences.get("categories", [])
            
            if not interests and not categories:
                # Return random articles if no preferences
                return self._get_trending_articles(top_k)
            
            # Build preference query
            preference_query = " ".join(interests + categories)
            
            # Transform preference query
            preference_vector = self.vectorizer.transform([preference_query])
            
            # Calculate similarity of all articles with preference vector
            similarity_scores = cosine_similarity(
                preference_vector,
                self.tfidf_matrix
            )[0]
            
            # Get top articles
            top_indices = np.argsort(similarity_scores)[::-1][:top_k]
            
            recommendations = []
            for idx in top_indices:
                article = self.articles[idx].copy()
                article["recommendation_score"] = round(float(similarity_scores[idx]), 3)
                recommendations.append(article)
            
            logger.info(f"Generated {len(recommendations)} personalized recommendations")
            return recommendations
        except Exception as e:
            logger.error(f"Error generating personalized recommendations: {str(e)}")
            return []
    
    def get_trending_articles(
        self,
        time_range_hours: int = 24,
        top_k: int = 10
    ) -> List[Dict]:
        """Get trending articles based on recency and relevance"""
        try:
            if not self.articles:
                return []
            
            from datetime import datetime, timedelta
            cutoff_time = datetime.utcnow() - timedelta(hours=time_range_hours)
            
            recent_articles = [
                article for article in self.articles
                if article.get("published_at")
            ]
            
            # Sort by publication date
            sorted_articles = sorted(
                recent_articles,
                key=lambda x: x.get("published_at", ""),
                reverse=True
            )
            
            return sorted_articles[:top_k]
        except Exception as e:
            logger.error(f"Error getting trending articles: {str(e)}")
            return []
    
    def _get_trending_articles(self, top_k: int = 10) -> List[Dict]:
        """Internal method to get trending articles"""
        return self.get_trending_articles(top_k=top_k)
    
    def _save_model(self) -> None:
        """Save trained model to disk"""
        try:
            os.makedirs(os.path.dirname(self.model_cache_path), exist_ok=True)
            with open(self.model_cache_path, 'wb') as f:
                pickle.dump({
                    'vectorizer': self.vectorizer,
                    'tfidf_matrix': self.tfidf_matrix,
                    'articles': self.articles,
                    'timestamp': datetime.utcnow().isoformat()
                }, f)
            logger.info(f"Model saved to {self.model_cache_path}")
        except Exception as e:
            logger.error(f"Error saving model: {str(e)}")
    
    def load_model(self) -> bool:
        """Load trained model from disk"""
        try:
            if os.path.exists(self.model_cache_path):
                with open(self.model_cache_path, 'rb') as f:
                    data = pickle.load(f)
                    self.vectorizer = data['vectorizer']
                    self.tfidf_matrix = data['tfidf_matrix']
                    self.articles = data['articles']
                    self.is_fitted = True
                logger.info("Model loaded successfully")
                return True
            return False
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            return False


class SimilarityCalculator:
    """Utility class for similarity calculations"""
    
    @staticmethod
    def cosine_similarity(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate cosine similarity between two vectors"""
        try:
            similarity = cosine_similarity([vec1], [vec2])[0][0]
            return float(similarity)
        except Exception as e:
            logger.error(f"Error calculating similarity: {str(e)}")
            return 0.0
    
    @staticmethod
    def jaccard_similarity(set1: set, set2: set) -> float:
        """Calculate Jaccard similarity between two sets"""
        if not set1 and not set2:
            return 1.0
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        if union == 0:
            return 0.0
        return float(intersection / union)
    
    @staticmethod
    def euclidean_distance(vec1: np.ndarray, vec2: np.ndarray) -> float:
        """Calculate Euclidean distance between vectors"""
        try:
            distance = np.linalg.norm(vec1 - vec2)
            return float(distance)
        except Exception as e:
            logger.error(f"Error calculating distance: {str(e)}")
            return float('inf')


class MEvaluationMetrics:
    """Metrics for evaluating recommendation quality"""
    
    @staticmethod
    def calculate_coverage(recommendations: List[Dict], total_items: int) -> float:
        """Calculate coverage (percentage of unique items recommended)"""
        if not recommendations or total_items == 0:
            return 0.0
        unique_items = len(set([r.get("id") for r in recommendations]))
        return float(unique_items / total_items)
    
    @staticmethod
    def calculate_diversity(recommendations: List[Dict]) -> float:
        """Calculate diversity of recommendations"""
        if len(recommendations) < 2:
            return 1.0
        
        categories = [r.get("category") for r in recommendations]
        unique_categories = len(set(categories))
        
        return float(unique_categories / len(recommendations))
    
    @staticmethod
    def calculate_precision_at_k(relevant_items: set, recommended_items: List[str], k: int) -> float:
        """Calculate Precision@K"""
        if k == 0:
            return 0.0
        recommended_at_k = set(recommended_items[:k])
        hits = len(recommended_at_k & relevant_items)
        return float(hits / k)
    
    @staticmethod
    def calculate_recall_at_k(relevant_items: set, recommended_items: List[str], k: int) -> float:
        """Calculate Recall@K"""
        if not relevant_items:
            return 0.0
        recommended_at_k = set(recommended_items[:k])
        hits = len(recommended_at_k & relevant_items)
        return float(hits / len(relevant_items))
