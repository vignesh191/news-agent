"""Client interface and convenience functions for the News Agent package."""

from typing import Optional

from utils.config import DEFAULT_MAX_RETRIES, DEFAULT_PAGE_SIZE, setup_logging
from core import NewsAgent
from data.exceptions import ConfigurationError, NewsAPIError
from data.models import NewsArticle

logger = setup_logging()


class NewsAgentClient:
    """
    Singleton-like client for easy access to NewsAgent functionality.
    Provides a clean interface while managing the underlying NewsAgent instance.
    """
    
    _instance = None
    
    @classmethod
    def get_instance(cls, news_api_key: Optional[str] = None, 
                     gemini_api_key: Optional[str] = None) -> NewsAgent:
        """
        Get or create a NewsAgent instance.
        
        Args:
            news_api_key: NewsAPI key (optional, reads from env if not provided)
            gemini_api_key: Gemini API key (optional, reads from env if not provided)
            
        Returns:
            NewsAgent instance
        """
        if cls._instance is None:
            cls._instance = NewsAgent(news_api_key, gemini_api_key)
        return cls._instance
    
    @classmethod
    def reset_instance(cls):
        """Reset the singleton instance (useful for testing)."""
        cls._instance = None


def get_daily_news(category: str = "business", use_youtube_summary: bool = True, 
                   page_size: int = DEFAULT_PAGE_SIZE, 
                   max_retries: int = DEFAULT_MAX_RETRIES) -> list[NewsArticle]:
    """
    Convenience function to get daily news articles.
    
    Args:
        category: News category to fetch
        use_youtube_summary: Whether to generate YouTube-style summaries
        page_size: Number of articles to successfully process
        max_retries: Maximum number of additional articles to try if some fail
        
    Returns:
        List of NewsArticle objects
    """
    client = NewsAgentClient.get_instance()
    return client.get_daily_news(category, use_youtube_summary, page_size, max_retries)


def main():
    """Main function for testing the API."""
    try:
        logger.info("Fetching business news with YouTube summaries...")
        news = get_daily_news(category="business", use_youtube_summary=True)
        
        print(f"Found {len(news)} articles:")
        for i, article in enumerate(news, 1):
            print(f"\n{i}. {article.title}")
            print(f"   Summary: {article.summary}")
            print(f"   Source: {article.source}")
            print(f"   Hashtags: {' '.join(article.hashtags)}")
        
    except (ConfigurationError, NewsAPIError) as e:
        logger.error(f"API error: {e}")
        print(f"Error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
