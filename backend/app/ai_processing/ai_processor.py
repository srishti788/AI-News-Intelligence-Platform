"""AI Processing Module using OpenAI"""
import logging
from openai import AsyncOpenAI
from typing import Dict, Optional, List
from app.config import settings
from textblob import TextBlob
import json

logger = logging.getLogger(__name__)

# Initialize OpenAI client
client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)


class AIProcessor:
    """Handle AI-powered content analysis"""
    
    def __init__(self):
        self.model = settings.OPENAI_MODEL
        self.max_tokens = 500
    
    async def summarize_article(self, title: str, content: str, style: str = "bullet") -> Dict:
        """Generate AI summary using OpenAI"""
        try:
            # Limit content length to avoid token limits
            max_chars = 2000
            content_chunk = content[:max_chars] if len(content) > max_chars else content
            
            prompt = f"""
            Summarize the following article in {style} format. Keep it concise and focus on key points.
            
            Title: {title}
            Content: {content_chunk}
            
            Provide a {style} format summary (2-4 points max).
            """
            
            response = await self._call_openai(prompt, max_tokens=200)
            
            return {
                "summary": response,
                "style": style,
                "model": self.model,
                "success": True
            }
        except Exception as e:
            logger.error(f"Error summarizing article: {str(e)}")
            return {
                "summary": self._fallback_summary(content),
                "success": False,
                "error": str(e)
            }
    
    async def extract_keywords(self, text: str, num_keywords: int = 5) -> List[str]:
        """Extract key concepts from text using AI"""
        try:
            prompt = f"""
            Extract the {num_keywords} most important keywords/concepts from this text.
            Return only the keywords as a JSON array of strings.
            
            Text: {text[:1500]}
            """
            
            response = await self._call_openai(prompt, max_tokens=100)
            
            # Parse JSON response
            try:
                keywords = json.loads(response)
                if isinstance(keywords, list):
                    return keywords[:num_keywords]
            except json.JSONDecodeError:
                # Fallback: split response by commas
                return [kw.strip() for kw in response.split(',')[:num_keywords]]
            
            return []
        except Exception as e:
            logger.error(f"Error extracting keywords: {str(e)}")
            return []
    
    async def analyze_sentiment(self, text: str) -> Dict:
        """Analyze sentiment of text"""
        try:
            # Use TextBlob for sentiment analysis (faster than API call)
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity  # -1 to 1
            subjectivity = blob.sentiment.subjectivity  # 0 to 1
            
            # Classify sentiment
            if polarity > 0.1:
                sentiment = "positive"
            elif polarity < -0.1:
                sentiment = "negative"
            else:
                sentiment = "neutral"
            
            return {
                "sentiment": sentiment,
                "polarity": round(polarity, 3),
                "subjectivity": round(subjectivity, 3),
                "confidence": round(abs(polarity), 3)
            }
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {str(e)}")
            return {
                "sentiment": "unknown",
                "polarity": 0,
                "subjectivity": 0.5,
                "confidence": 0,
                "error": str(e)
            }
    
    async def answer_question(self, question: str, context: List[Dict]) -> Dict:
        """Answer user question based on news articles - with fallback"""
        try:
            # Try to use OpenAI if available
            try:
                # Prepare context from articles
                context_text = "\n\n".join([
                    f"- {article.get('title', '')}: {article.get('content', '')[:300]}"
                    for article in context[:5]  # Limit to 5 articles
                ])
                
                prompt = f"""
                Based on the following news articles, answer the user's question.
                Be concise and cite sources when possible.
                
                Context:
                {context_text}
                
                Question: {question}
                
                Answer:
                """
                
                response = await self._call_openai(prompt, max_tokens=300)
                
                return {
                    "answer": response,
                    "question": question,
                    "success": True,
                    "source": "OpenAI"
                }
            except Exception as openai_error:
                logger.warning(f"OpenAI call failed, using fallback: {str(openai_error)}")
                # Fallback to local answer extraction
                return self._answer_question_local(question, context)
                
        except Exception as e:
            logger.error(f"Error answering question: {str(e)}")
            return {
                "answer": f"Unable to answer question: {str(e)}",
                "question": question,
                "success": False
            }
    
    def _answer_question_local(self, question: str, context: List[Dict]) -> Dict:
        """Answer question using local article content (no API calls)"""
        try:
            # Extract relevant articles based on question keywords
            question_words = set(question.lower().split())
            scored_articles = []
            
            for article in context:
                title = article.get('title', '').lower()
                content = article.get('content', '').lower()
                description = article.get('description', '').lower()
                
                # Simple scoring: count matching keywords
                full_text = f"{title} {content} {description}"
                score = sum(1 for word in question_words if word in full_text)
                
                if score > 0:
                    scored_articles.append((score, article))
            
            # Sort by relevance
            scored_articles.sort(key=lambda x: x[0], reverse=True)
            
            # Build answer from top articles
            answer_parts = []
            for score, article in scored_articles[:3]:  # Use top 3 articles
                title = article.get('title', 'Unknown')
                content = article.get('content', article.get('description', 'No details'))
                
                # Extract first 200 chars of content
                content_summary = content[:200].strip()
                if not content_summary.endswith('.'):
                    content_summary += '...'
                
                answer_parts.append(f"• {title}: {content_summary}")
            
            if answer_parts:
                answer = "Based on current news:\n\n" + "\n\n".join(answer_parts)
            else:
                # No relevant articles found
                all_titles = [a.get('title', 'Unknown') for a in context[:3]]
                answer = f"Related to your question, here are the latest news: {', '.join(all_titles)}"
            
            return {
                "answer": answer,
                "question": question,
                "success": True,
                "source": "Local (News Articles)"
            }
        except Exception as e:
            logger.error(f"Error in local answer generation: {str(e)}")
            return {
                "answer": "I found news articles but couldn't generate a specific answer. Try searching for news directly.",
                "question": question,
                "success": False,
                "source": "Fallback"
            }

    
    async def _call_openai(self, prompt: str, max_tokens: int = 500) -> str:
        """Call OpenAI API"""
        try:
            response = await client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert news analyst. Provide clear, concise, and accurate information."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=max_tokens,
                temperature=0.7,
                timeout=30
            )
            
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
    
    @staticmethod
    def _fallback_summary(content: str, num_sentences: int = 3) -> str:
        """Fallback summary using TextBlob when AI is unavailable"""
        try:
            sentences = content.split('.')
            if len(sentences) <= num_sentences:
                return content
            
            # Use TextBlob's naive summarization
            blob = TextBlob(content)
            sentences = blob.sentences
            
            if len(sentences) > num_sentences:
                return ' '.join([str(s) for s in sentences[:num_sentences]])
            return content
        except Exception as e:
            logger.error(f"Error in fallback summary: {str(e)}")
            return content[:500] + "..."


class ContentAnalyzer:
    """Advanced content analysis"""
    
    @staticmethod
    def extract_entities(text: str) -> Dict:
        """Extract named entities from text"""
        # Simplified entity extraction
        entities = {
            "people": [],
            "organizations": [],
            "locations": [],
            "dates": []
        }
        
        try:
            # Simple pattern matching for common entity types
            import re
            
            # Find all capitalized words (potential names)
            words = text.split()
            capitalized = [word for word in words if word and word[0].isupper()]
            
            # Extract unique capitalized words longer than 2 chars
            entities["potential_entities"] = list(set(
                [word for word in capitalized if len(word) > 2][:10]
            ))
            
            return entities
        except Exception as e:
            logger.error(f"Error extracting entities: {str(e)}")
            return entities
    
    @staticmethod
    def evaluate_article_quality(article: Dict) -> Dict:
        """Evaluate article quality metrics"""
        content = article.get("content", "")
        title = article.get("title", "")
        
        metrics = {
            "content_length": len(content),
            "word_count": len(content.split()),
            "title_length": len(title),
            "has_url": bool(article.get("url")),
            "has_author": bool(article.get("author") and article.get("author") != "Unknown"),
            "has_publication_date": bool(article.get("published_at")),
            "quality_score": 0
        }
        
        # Calculate quality score
        score = 0
        if metrics["content_length"] > 500:
            score += 25
        if metrics["word_count"] > 100:
            score += 25
        if metrics["has_url"]:
            score += 15
        if metrics["has_author"]:
            score += 15
        if metrics["has_publication_date"]:
            score += 20
        
        metrics["quality_score"] = min(100, score)
        
        return metrics
