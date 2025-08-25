"""
News Agent API - A clean interface for fetching and summarizing news articles.

This module provides backward compatibility while using the new modular structure.
For new projects, import directly from the newsagent package.
"""

# Import everything from the new modular structure
from newsagent import (
    NewsAPIClient,
    get_daily_news,
    NewsArticle,
    ArticleContent,
    NewsAPIError,
    ConfigurationError,
    ArticleProcessingError
)

# For backward compatibility, expose the main NewsAPI class
from newsagent.core import NewsAPI

# Main function for testing
main = lambda: __import__('newsagent.client', fromlist=['main']).main()

if __name__ == "__main__":
    main()

