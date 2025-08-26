"""
NewsAgent - A clean API for fetching and summarizing news articles for TikTok content creation.

This package provides a modular structure for fetching news articles, processing content,
and generating TikTok-style summaries using various AI services.

Main usage:
    from client import get_daily_news
    articles = get_daily_news("technology", page_size=5)
"""

from client import get_daily_news
from data.models import NewsArticle

__version__ = "1.0.0"
__all__ = [
    "get_daily_news",
    "NewsArticle"
]

# Advanced users can import specific modules:
# from client import NewsAgentClient
# from data.exceptions import NewsAPIError, ConfigurationError
# from core import NewsAgent
