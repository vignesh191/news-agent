"""Custom exceptions for the News Agent package."""


class NewsAPIError(Exception):
    """Base exception for NewsAPI related errors."""
    pass


class ConfigurationError(NewsAPIError):
    """Raised when configuration is invalid."""
    pass


class ArticleProcessingError(NewsAPIError):
    """Raised when article processing fails."""
    pass
