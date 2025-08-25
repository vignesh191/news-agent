"""News fetching and API integration modules."""

import logging
from typing import Optional

from newsapi import NewsApiClient

from ..utils.config import (
    DEFAULT_COUNTRY, DEFAULT_LANGUAGE, API_PAGE_SIZE_LIMIT
)
from ..data.exceptions import NewsAPIError

logger = logging.getLogger(__name__)


class NewsFetcher:
    """Handles fetching news articles from the NewsAPI service."""
    
    def __init__(self, api_key: str):
        """
        Initialize the news fetcher.
        
        Args:
            api_key: NewsAPI key
        """
        self.api_key = api_key
        self._client = None
    
    @property
    def client(self) -> NewsApiClient:
        """Lazy initialization of NewsAPI client."""
        if self._client is None:
            self._client = NewsApiClient(api_key=self.api_key)
            logger.debug("NewsAPI client initialized")
        return self._client
    
    def get_top_headlines(self, category: str, page_size: int = 5, 
                          language: str = DEFAULT_LANGUAGE, 
                          country: str = DEFAULT_COUNTRY) -> list[dict]:
        """
        Fetch top headlines from NewsAPI for a given category.
        
        Args:
            category: News category (business, technology, etc.)
            page_size: Number of articles to fetch
            language: Language code
            country: Country code
            
        Returns:
            List of article dictionaries
            
        Raises:
            NewsAPIError: If the API request fails
        """
        try:
            response = self.client.get_top_headlines(
                language=language,
                country=country,
                page_size=min(page_size, API_PAGE_SIZE_LIMIT),
                category=category
            )
            articles = response.get('articles', [])
            logger.info(f"Fetched {len(articles)} headlines for category '{category}'")
            return articles

        except Exception as e:
            logger.error(f"Error fetching headlines for category '{category}': {e}")
            raise NewsAPIError(f"Failed to fetch headlines: {e}")
    
    def get_additional_headlines(self, category: str, exclude_urls: set, 
                                page_size: int = 20,
                                language: str = DEFAULT_LANGUAGE, 
                                country: str = DEFAULT_COUNTRY) -> list[dict]:
        """
        Fetch additional headlines excluding already processed URLs.
        
        Args:
            category: News category
            exclude_urls: Set of URLs to exclude from results
            page_size: Number of articles to fetch
            language: Language code
            country: Country code
            
        Returns:
            List of article dictionaries excluding already processed URLs
        """
        try:
            response = self.client.get_top_headlines(
                language=language,
                country=country,
                page_size=min(page_size, API_PAGE_SIZE_LIMIT),
                category=category
            )
            articles = response.get('articles', [])
            
            # Filter out already processed URLs
            filtered_articles = [
                article for article in articles 
                if article.get('url') and article.get('url') not in exclude_urls
            ]
            
            logger.info(f"Fetched {len(filtered_articles)} additional headlines for category '{category}'")
            return filtered_articles

        except Exception as e:
            logger.warning(f"Error fetching additional headlines for category '{category}': {e}")
            return []
