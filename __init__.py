"""
NewsAgent - A clean API for fetching and summarizing news articles for TikTok content creation.

This package provides a modular structure for fetching news articles, processing content,
and generating TikTok-style summaries using various AI services.
"""

from client import NewsAPIClient, get_daily_news
from data import NewsArticle, ArticleContent, NewsAPIError, ConfigurationError, ArticleProcessingError

__version__ = "1.0.0"
__all__ = [
    "NewsAPIClient",
    "get_daily_news", 
    "NewsArticle",
    "ArticleContent",
    "NewsAPIError",
    "ConfigurationError", 
    "ArticleProcessingError"
]
