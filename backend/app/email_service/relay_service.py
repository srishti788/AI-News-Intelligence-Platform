"""Email Service Integration with Relay.app"""
import logging
import aiohttp
import json
from typing import Dict, List, Optional
from datetime import datetime
from app.config import settings

logger = logging.getLogger(__name__)


class RelayEmailService:
    """Service for sending emails via Relay.app webhook"""
    
    def __init__(self):
        self.webhook_url = settings.RELAY_WEBHOOK_URL
        self.api_key = settings.RELAY_API_KEY
    
    async def send_email(
        self,
        recipient_email: str,
        subject: str,
        template_id: str,
        variables: Dict
    ) -> Dict:
        """Send email via Relay.app webhook"""
        try:
            if not self.webhook_url:
                logger.warning("Relay webhook URL not configured")
                return {"success": False, "error": "Webhook not configured"}
            
            payload = {
                "to": recipient_email,
                "subject": subject,
                "template_id": template_id,
                "variables": variables,
                "timestamp": datetime.utcnow().isoformat()
            }
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self.api_key}" if self.api_key else None
            }
            
            # Remove None values from headers
            headers = {k: v for k, v in headers.items() if v}
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.webhook_url,
                    json=payload,
                    headers=headers,
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    result = await response.json()
                    
                    if response.status in [200, 201, 202]:
                        logger.info(f"Email sent successfully to {recipient_email}")
                        return {"success": True, "response": result}
                    else:
                        logger.error(f"Failed to send email: {result}")
                        return {"success": False, "error": str(result)}
        
        except Exception as e:
            logger.error(f"Error sending email via Relay: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def send_news_digest(
        self,
        recipient_email: str,
        articles: List[Dict],
        user_name: str = "User"
    ) -> Dict:
        """Send daily news digest email"""
        try:
            subject = f"Daily News Digest - {datetime.utcnow().strftime('%B %d, %Y')}"
            
            # Prepare article variables for email template
            articles_html = self._format_articles_for_email(articles)
            
            variables = {
                "user_name": user_name,
                "articles_count": len(articles),
                "articles_html": articles_html,
                "date": datetime.utcnow().strftime('%B %d, %Y'),
                "unsubscribe_url": f"https://news-intelligence-platform.com/unsubscribe?email={recipient_email}"
            }
            
            return await self.send_email(
                recipient_email=recipient_email,
                subject=subject,
                template_id="daily_news_digest",
                variables=variables
            )
        except Exception as e:
            logger.error(f"Error sending news digest: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def _format_articles_for_email(self, articles: List[Dict]) -> str:
        """Format articles as HTML for email template"""
        try:
            html = ""
            for article in articles[:10]:  # Limit to 10 articles
                html += f"""
                <div style="margin-bottom: 20px; padding-bottom: 20px; border-bottom: 1px solid #eee;">
                    <h3 style="margin: 0 0 10px 0; color: #333;">
                        <a href="{article.get('url', '#')}" style="text-decoration: none; color: #2563eb;">
                            {article.get('title', 'No Title')}
                        </a>
                    </h3>
                    <p style="margin: 0 0 5px 0; color: #666; font-size: 0.9em;">
                        {article.get('source', 'Unknown Source')} · {article.get('published_at', 'Unknown Date')}
                    </p>
                    <p style="margin: 0 0 10px 0; color: #666;">
                        {article.get('summary', article.get('content', '')[:200])}
                    </p>
                    <a href="{article.get('url', '#')}" style="color: #2563eb; text-decoration: none; font-size: 0.9em;">
                        Read more →
                    </a>
                </div>
                """
            
            return html
        except Exception as e:
            logger.error(f"Error formatting articles: {str(e)}")
            return ""


class EmailTemplate:
    """Email template management"""
    
    DAILY_DIGEST_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; background-color: #f5f5f5; }}
            .container {{ max-width: 600px; margin: 20px auto; background-color: white; padding: 20px; border-radius: 8px; }}
            .header {{ background-color: #2563eb; color: white; padding: 20px; text-align: center; border-radius: 8px; }}
            .footer {{ background-color: #f9fafb; padding: 15px; text-align: center; font-size: 0.9em; color: #666; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>Your Daily News Intelligence Digest</h1>
                <p>{date}</p>
            </div>
            
            <div style="padding: 20px 0;">
                <h2>Hello {user_name}!</h2>
                <p>Here are your top {articles_count} personalized news articles for today:</p>
                
                {articles_html}
            </div>
            
            <div class="footer">
                <p>© 2024 News Intelligence Platform</p>
                <p>
                    <a href="{unsubscribe_url}" style="color: #2563eb; text-decoration: none;">Unsubscribe</a>
                </p>
            </div>
        </div>
    </body>
    </html>
    """
    
    SUMMARY_NOTIFICATION_TEMPLATE = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            .alert {{ background-color: #dbeafe; border-left: 4px solid #2563eb; padding: 15px; margin: 10px 0; }}
        </style>
    </head>
    <body>
        <div style="max-width: 600px; margin: 20px auto;">
            <h2>New Article Summary: {title}</h2>
            <div class="alert">
                <h3>{article_title}</h3>
                <p>{summary}</p>
                <p><strong>Sentiment:</strong> {sentiment}</p>
                <a href="{url}">Read Full Article</a>
            </div>
        </div>
    </body>
    </html>
    """


class SMTPEmailService:
    """Fallback SMTP email service (if Relay is not available)"""
    
    def __init__(self):
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.username = settings.SMTP_USERNAME
        self.password = settings.SMTP_PASSWORD
        self.from_email = settings.FROM_EMAIL
    
    async def send_email(self, to_email: str, subject: str, body: str) -> Dict:
        """Send email via SMTP"""
        try:
            if not all([self.smtp_server, self.username, self.password, self.from_email]):
                logger.warning("SMTP not properly configured")
                return {"success": False, "error": "SMTP not configured"}
            
            import smtplib
            from email.mime.text import MIMEText
            from email.mime.multipart import MIMEMultipart
            
            message = MIMEMultipart("alternative")
            message["Subject"] = subject
            message["From"] = self.from_email
            message["To"] = to_email
            
            part = MIMEText(body, "html")
            message.attach(part)
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.username, self.password)
                server.sendmail(self.from_email, to_email, message.as_string())
            
            logger.info(f"Email sent via SMTP to {to_email}")
            return {"success": True}
        except Exception as e:
            logger.error(f"Error sending email via SMTP: {str(e)}")
            return {"success": False, "error": str(e)}


class EmailScheduler:
    """Schedule and manage email sending"""
    
    def __init__(self, relay_service: RelayEmailService):
        self.relay_service = relay_service
        self.scheduled_emails = []
    
    async def schedule_daily_digest(
        self,
        user_email: str,
        user_name: str,
        articles: List[Dict],
        send_time: str = "09:00"
    ) -> Dict:
        """Schedule daily digest email"""
        try:
            return await self.relay_service.send_news_digest(
                recipient_email=user_email,
                articles=articles,
                user_name=user_name
            )
        except Exception as e:
            logger.error(f"Error scheduling digest: {str(e)}")
            return {"success": False, "error": str(e)}
    
    async def send_breaking_news_alert(
        self,
        user_email: str,
        article: Dict
    ) -> Dict:
        """Send breaking news alert"""
        try:
            subject = f"Breaking: {article.get('title', 'News Alert')}"
            variables = {
                "article_title": article.get("title"),
                "summary": article.get("summary", article.get("content", "")[:200]),
                "url": article.get("url"),
                "sentiment": article.get("sentiment", "neutral")
            }
            
            return await self.relay_service.send_email(
                recipient_email=user_email,
                subject=subject,
                template_id="breaking_news_alert",
                variables=variables
            )
        except Exception as e:
            logger.error(f"Error sending alert: {str(e)}")
            return {"success": False, "error": str(e)}
