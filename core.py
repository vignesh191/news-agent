"""Core NewsAPI class that orchestrates all services."""

from typing import Optional

from services.ai_services import GeminiSummarizer
from services.news_fetcher import NewsFetcher
from services.processors import ArticleProcessor, HashtagGenerator
from data.exceptions import ConfigurationError, NewsAPIError
from data.models import ArticleContent, NewsArticle
from utils.config import (
    DEFAULT_MAX_HASHTAGS, DEFAULT_MAX_RETRIES, DEFAULT_PAGE_SIZE,
    setup_logging
)

logger = setup_logging()


class NewsAgent:
    """
    Core API class for fetching and summarizing news articles for YouTube content creation.
    
    This class orchestrates all services including news fetching, content processing,
    and AI-powered summarization.
    """
    
    def __init__(self, news_api_key: Optional[str] = None, gemini_api_key: Optional[str] = None):
        """
        Initialize the NewsAPI with required API keys.
        
        Args:
            news_api_key: NewsAPI key (if not provided, reads from environment)
            gemini_api_key: Gemini API key (if not provided, reads from environment)
            
        Raises:
            ConfigurationError: If required API keys are missing
        """
        # Get API keys from environment if not provided
        if not news_api_key or not gemini_api_key:
            from utils.config import get_api_keys
            try:
                env_news_key, env_gemini_key = get_api_keys()
                news_api_key = news_api_key or env_news_key
                gemini_api_key = gemini_api_key or env_gemini_key
            except ValueError as e:
                raise ConfigurationError(str(e))
        
        # Initialize services
        self._news_fetcher = NewsFetcher(news_api_key)
        self._article_processor = ArticleProcessor()
        self._gemini_summarizer = GeminiSummarizer(gemini_api_key)
        self._hashtag_generator = HashtagGenerator()
        
        logger.info("NewsAPI initialized successfully")
    
    # News fetching methods
    def get_top_headlines(self, category: str, page_size: int = DEFAULT_PAGE_SIZE, 
                          language: str = 'en', country: str = 'us') -> list[dict]:
        """Fetch top headlines from NewsAPI."""
        return self._news_fetcher.get_top_headlines(category, page_size, language, country)
    
    def get_additional_headlines(self, category: str, exclude_urls: set, 
                                page_size: int = 20, language: str = 'en', 
                                country: str = 'us') -> list[dict]:
        """Fetch additional headlines excluding already processed URLs."""
        return self._news_fetcher.get_additional_headlines(
            category, exclude_urls, page_size, language, country
        )
    
    # Content processing methods
    def get_article_content(self, url: str) -> Optional[ArticleContent]:
        """Extract article content from URL."""
        try:
            return self._article_processor.extract_content(url)
        except Exception:
            return None
    
    def generate_youtube_summary(self, text: str, max_length: int = 3000) -> str:
        """Generate YouTube-style summary using Gemini."""
        return self._gemini_summarizer.generate_youtube_summary(text, max_length)
    
    def generate_hashtags(self, url: str, category: str, 
                         article_content: Optional[ArticleContent] = None,
                         max_hashtags: int = DEFAULT_MAX_HASHTAGS) -> list[str]:
        """Generate hashtags from article content and category."""
        if article_content is None:
            article_content = self.get_article_content(url)
        
        return self._hashtag_generator.generate(
            category, article_content, max_hashtags
        )
    
    # Main processing methods
    def _process_single_article(self, article: dict, category: str, 
                               use_youtube_summary: bool) -> Optional[NewsArticle]:
        """Process a single article and return NewsArticle object if successful."""
        try:
            # Extract basic info
            title = article.get('title', 'No title available')
            source = article.get('source', {}).get('name', 'Unknown source')
            published_at = article.get('publishedAt', '')
            url = article.get('url', '')
            
            if not url:
                logger.warning(f"Skipping article without URL: {title}")
                return None
            
            # Fetch full article content
            parsed_article = self.get_article_content(url)
            
            if not parsed_article:
                summary = article.get('description', 'No summary available')
                logger.warning(f"Could not parse article content for: {title}")
            else:
                if use_youtube_summary:
                    summary = self.generate_youtube_summary(parsed_article.text)
                else:
                    summary = parsed_article.summary or 'No summary available'
            
            hashtags = self.generate_hashtags(url, category, parsed_article)
            
            return NewsArticle(
                title=title,
                summary=summary,
                source=source,
                published_at=published_at,
                hashtags=hashtags,
                url=url
            )
            
        except Exception as e:
            logger.error(f"Error processing article '{title}': {e}")
            return None

    def get_daily_news(self, category: str = "business", use_youtube_summary: bool = True, 
                       page_size: int = DEFAULT_PAGE_SIZE, 
                       max_retries: int = DEFAULT_MAX_RETRIES) -> list[NewsArticle]:
        """
        Main API method to get daily news articles with summaries and hashtags.
        Automatically retries with additional articles if some fail to download.
        
        Args:
            category: News category to fetch
            use_youtube_summary: Whether to generate YouTube-style summaries
            page_size: Number of articles to successfully process
            max_retries: Maximum number of additional articles to try if some fail
            
        Returns:
            List of NewsArticle objects (up to page_size articles)
            
        Raises:
            NewsAPIError: If fetching headlines fails
        """
        articles_data = []
        processed_urls = set()
        
        try:
            # Fetch initial headlines
            headlines = self.get_top_headlines(category, page_size=page_size)
            
            if not headlines:
                logger.warning(f"No headlines found for category: {category}")
                return []
            
            logger.info(f"Processing {len(headlines)} initial articles for category: {category}")
            
            # Process initial batch of articles
            for article in headlines:
                url = article.get('url', '')
                if url:
                    processed_urls.add(url)
                
                processed_article = self._process_single_article(article, category, use_youtube_summary)
                if processed_article:
                    articles_data.append(processed_article)
                
                # Stop if we have enough successful articles
                if len(articles_data) >= page_size:
                    break
            
            # If we don't have enough articles, try to get more
            retry_count = 0
            while len(articles_data) < page_size and retry_count < max_retries:
                logger.info(f"Need {page_size - len(articles_data)} more articles. Fetching additional headlines...")
                
                # Fetch additional headlines excluding already processed URLs
                additional_headlines = self.get_additional_headlines(
                    category, 
                    exclude_urls=processed_urls,
                    page_size=20  # Fetch more to have better chances
                )
                
                if not additional_headlines:
                    logger.warning("No additional headlines available")
                    break
                
                # Process additional articles
                for article in additional_headlines:
                    url = article.get('url', '')
                    if url:
                        processed_urls.add(url)
                    
                    processed_article = self._process_single_article(article, category, use_youtube_summary)
                    if processed_article:
                        articles_data.append(processed_article)
                    
                    retry_count += 1
                    
                    # Stop if we have enough successful articles or hit retry limit
                    if len(articles_data) >= page_size or retry_count >= max_retries:
                        break
                
                if not additional_headlines:
                    break
            
            final_count = len(articles_data)
            if final_count < page_size:
                logger.warning(f"Only successfully processed {final_count} articles out of requested {page_size}")
            else:
                logger.info(f"Successfully processed {final_count} articles as requested")
            
            return articles_data[:page_size]  # Ensure we don't exceed requested count
            
        except NewsAPIError:
            raise
        except Exception as e:
            logger.error(f"Unexpected error in get_daily_news: {e}")
            raise NewsAPIError(f"Failed to get daily news: {e}")
