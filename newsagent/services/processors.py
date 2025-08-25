"""Article processing and content extraction modules."""

import logging
from functools import lru_cache
from typing import Optional

import nltk
from newspaper import Article

from ..utils.config import CACHE_SIZE
from ..data.exceptions import ArticleProcessingError
from ..data.models import ArticleContent

logger = logging.getLogger(__name__)

# Download NLTK data once
try:
    nltk.download('punkt_tab', quiet=True)
except Exception as e:
    logger.warning(f"Failed to download NLTK data: {e}")


class ArticleProcessor:
    """Handles article content extraction and processing with caching."""
    
    def __init__(self):
        """Initialize the article processor."""
        logger.debug("ArticleProcessor initialized")
    
    @lru_cache(maxsize=CACHE_SIZE)
    def extract_content(self, url: str) -> Optional[ArticleContent]:
        """
        Extract content from a news article URL with caching.
        
        Args:
            url: The URL of the article to process
            
        Returns:
            ArticleContent object if successful, None otherwise
            
        Raises:
            ArticleProcessingError: If article processing fails
        """
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()
            
            content = ArticleContent(
                text=article.text,
                keywords=article.keywords or [],
                summary=article.summary or "",
                url=url
            )
            
            logger.debug(f"Successfully extracted content from {url}")
            return content
            
        except Exception as e:
            logger.error(f"Failed to process article from {url}: {e}")
            raise ArticleProcessingError(f"Could not process article: {e}")


class HashtagGenerator:
    """Generates hashtags from article content and categories."""
    
    @staticmethod
    def generate(category: str, article_content: Optional[ArticleContent] = None,
                max_hashtags: int = 10) -> list[str]:
        """
        Generate hashtags from article content and category.
        
        Args:
            category: The news category
            article_content: Pre-extracted article content (optional)
            max_hashtags: Maximum number of hashtags to return
            
        Returns:
            List of hashtags with # prefix
        """
        hashtags = [f"#{category}"]  # Always include category
        
        if article_content and article_content.keywords:
            # Filter and format keywords
            keyword_hashtags = [
                f"#{keyword.replace(' ', '').lower()}" 
                for keyword in article_content.keywords[:max_hashtags-1]
                if keyword and len(keyword) > 2  # Filter out short keywords
            ]
            hashtags.extend(keyword_hashtags)
        
        return hashtags[:max_hashtags]
