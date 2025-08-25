"""Utils module for NewsAgent - Configuration and utility functions."""

from .config import (
    DEFAULT_PAGE_SIZE,
    DEFAULT_MAX_RETRIES, 
    DEFAULT_MAX_HASHTAGS,
    setup_logging,
    get_api_keys
)

__all__ = [
    "DEFAULT_PAGE_SIZE",
    "DEFAULT_MAX_RETRIES",
    "DEFAULT_MAX_HASHTAGS", 
    "setup_logging",
    "get_api_keys"
]
