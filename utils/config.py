"""Configuration and constants for the News Agent package."""

import os
import logging
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Default configuration
DEFAULT_PAGE_SIZE = 5
DEFAULT_MAX_RETRIES = 10
DEFAULT_MAX_HASHTAGS = 5
DEFAULT_TEXT_MAX_LENGTH = 16000  # Optimized for Gemini 2.0
DEFAULT_LANGUAGE = 'en'
DEFAULT_COUNTRY = 'us'
API_PAGE_SIZE_LIMIT = 100
CACHE_SIZE = 128

# TEXT_MAX_LENGTH Explanation:
# - Gemini 2.0 Flash Exp supports 2M tokens input (~1.5M words)
# - Average news article: 1000-3000 words
# - 16000 characters ≈ 2500-4000 words (depending on complexity)
# - Leaves plenty of room for prompt + article content
# - Captures full article content for most news pieces
# - Safe margin below API limits

# Gemini model configuration
GEMINI_MODEL = "gemini-2.0-flash-exp"

# TikTok prompt template
TIKTOK_PROMPT_TEMPLATE = """
You are a TikTok content creator targeting a Gen-Z audience. 
Summarize the following news article in 3–4 trendy and easy-to-understand sentences. 
- Make it fun and conversational, with a touch of witty humor. 
- Keep the audience engaged; views are the goal. 
- Focus on the main points and avoid unnecessary details.
- Stick to the facts of the article and provide accurate information.
- Make it perfect for reading aloud in a TikTok video.
- Do not use any hashtags.
- Return only the summary, no boilerplate. 
- Do not use any emojis.

Article:
{text}
"""

# Logging configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


def setup_logging(level: int = logging.INFO) -> logging.Logger:
    """Configure and return logger for the package."""
    logging.basicConfig(level=level, format=LOG_FORMAT)
    return logging.getLogger(__name__)


def get_api_keys() -> tuple[str, str]:
    """
    Get API keys from environment variables.
    
    Returns:
        Tuple of (news_api_key, gemini_api_key)
        
    Raises:
        ValueError: If required API keys are missing
    """
    news_api_key = os.getenv("NEWS_API_KEY")
    gemini_api_key = os.getenv("GEMINI_API_KEY")
    
    if not news_api_key:
        raise ValueError("NEWS_API_KEY environment variable is required")
    if not gemini_api_key:
        raise ValueError("GEMINI_API_KEY environment variable is required")
        
    return news_api_key, gemini_api_key
