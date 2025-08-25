"""Data models for the News Agent package."""

from dataclasses import dataclass


@dataclass
class ArticleContent:
    """Data class for article content extracted from URLs."""
    text: str
    keywords: list[str]
    summary: str
    url: str


@dataclass
class NewsArticle:
    """Data class for processed news articles ready for consumption."""
    title: str
    summary: str
    source: str
    published_at: str
    hashtags: list[str]
    url: str
