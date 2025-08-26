"""AI services for content generation and summarization."""

import logging
from typing import Optional

from google import genai

from utils.config import GEMINI_MODEL, YOUTUBE_PROMPT_TEMPLATE, DEFAULT_TEXT_MAX_LENGTH

logger = logging.getLogger(__name__)


class GeminiSummarizer:
    """Handles YouTube-style content summarization using Google's Gemini AI."""
    
    def __init__(self, api_key: str):
        """
        Initialize the Gemini summarizer.
        
        Args:
            api_key: Gemini API key
        """
        self.api_key = api_key
        self._client = None
    
    @property
    def client(self) -> genai.Client:
        """Lazy initialization of Gemini client."""
        if self._client is None:
            self._client = genai.Client(api_key=self.api_key)
            logger.debug("Gemini client initialized")
        return self._client
    
    def generate_youtube_summary(self, text: str, max_length: int = DEFAULT_TEXT_MAX_LENGTH) -> str:
        """
        Generate YouTube-style summary using Gemini.
        
        Args:
            text: The article text to summarize
            max_length: Maximum text length to send to AI
            
        Returns:
            YouTube-style summary string
        """
        if not text:
            return "No content available"
        
        prompt = YOUTUBE_PROMPT_TEMPLATE.format(text=text[:max_length])
        
        try:
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt
            )
            summary = response.text.strip()
            logger.info("Generated YouTube summary successfully")
            return summary
            
        except Exception as e:
            logger.error(f"Error generating YouTube summary: {e}")
            return "Summary generation failed"
