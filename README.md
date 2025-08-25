# News Agent 📰

A clean, modular API for fetching and summarizing news articles for TikTok content creation. This package provides news fetching, content processing, and AI-powered summarization with automatic retry mechanisms for robust article processing.

## ✨ Features

- **🔄 Automatic Retry Logic**: Fetches additional articles if some fail to download
- **🤖 AI-Powered Summaries**: TikTok-style content generation using Google's Gemini AI
- **📊 Smart Caching**: LRU cache for article processing to improve performance
- **🏷️ Hashtag Generation**: Automatic hashtag creation from article keywords
- **📦 Modular Design**: Clean separation of concerns with dedicated modules
- **🛡️ Robust Error Handling**: Custom exceptions and comprehensive logging
- **⚡ Lazy Loading**: API clients initialized only when needed

## 🚀 Quick Start

### Installation

```bash
pip install -r requirements.txt
```

### Environment Setup

Create a `.env` file:

```bash
NEWS_API_KEY=your_newsapi_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### Simple Usage

```python
from newsagent import get_daily_news

# Get 5 business articles with TikTok summaries
articles = get_daily_news(
    category="business",
    use_tiktok_summary=True,
    page_size=5
)

for article in articles:
    print(f"Title: {article.title}")
    print(f"Summary: {article.summary}")
    print(f"Hashtags: {', '.join(article.hashtags)}")
```

## 📖 API Reference

### Main Functions

#### `get_daily_news(category, use_tiktok_summary, page_size, max_retries)`

Convenience function to get daily news articles.

**Parameters:**
- `category` (str): News category (business, technology, sports, etc.)
- `use_tiktok_summary` (bool): Whether to generate TikTok-style summaries
- `page_size` (int): Number of articles to successfully process (default: 5)
- `max_retries` (int): Maximum additional articles to try if some fail (default: 10)

**Returns:** List of `NewsArticle` objects

### Classes

#### `NewsAPIClient`

Singleton-like client for easy access to NewsAPI functionality.

```python
from newsagent import NewsAPIClient

client = NewsAPIClient.get_instance()
articles = client.get_daily_news("technology", page_size=3)
```

#### `NewsAPI`

Core API class for advanced usage and custom configuration.

```python
from newsagent.core import NewsAPI

api = NewsAPI(news_api_key="your_key", gemini_api_key="your_key")
articles = api.get_daily_news("science", max_retries=20)
```

### Data Models

#### `NewsArticle`

```python
@dataclass
class NewsArticle:
    title: str
    summary: str
    source: str
    published_at: str
    hashtags: List[str]
    url: str
```

#### `ArticleContent`

```python
@dataclass
class ArticleContent:
    text: str
    keywords: List[str]
    summary: str
    url: str
```

## 🏗️ Architecture

The package is organized into focused modules with logical subdirectories:

```
newsagent/
├── __init__.py          # Package interface and main exports
├── client.py            # Client interface and convenience functions
├── core.py              # Main NewsAPI orchestration class
├── data/                # Data models and exceptions
│   ├── __init__.py      # Data module exports
│   ├── models.py        # NewsArticle and ArticleContent dataclasses
│   └── exceptions.py    # Custom exception definitions
├── services/            # External integrations and processing
│   ├── __init__.py      # Services module exports
│   ├── ai_services.py   # Gemini AI summarization service
│   ├── news_fetcher.py  # NewsAPI integration and fetching
│   └── processors.py    # Article processing and hashtag generation
└── utils/               # Utilities and configuration
    ├── __init__.py      # Utils module exports
    └── config.py        # Configuration constants and setup
```

### 📁 **Detailed File Descriptions**

#### **Root Level**
- **`__init__.py`** - Main package interface exposing the most commonly used classes and functions
- **`client.py`** - High-level client class with singleton pattern and convenience functions for easy usage
- **`core.py`** - Central orchestrator that coordinates all services and implements the main business logic

#### **`data/` - Data Layer**
- **`models.py`** - Dataclass definitions for `NewsArticle` (final output) and `ArticleContent` (raw processed content)
- **`exceptions.py`** - Custom exception hierarchy: `NewsAPIError`, `ConfigurationError`, `ArticleProcessingError`

#### **`services/` - Service Layer**  
- **`ai_services.py`** - Gemini AI integration for generating TikTok-style summaries with configurable prompts
- **`news_fetcher.py`** - NewsAPI client wrapper handling headline fetching, pagination, and URL deduplication
- **`processors.py`** - Article content extraction using newspaper3k, hashtag generation, and caching logic

#### **`utils/` - Utility Layer**
- **`config.py`** - Centralized configuration management, environment variable handling, logging setup, and constants

#### **Support Files**
- **`api.py`** - Backward compatibility layer that re-exports everything from the new structure
- **`example.py`** - Comprehensive usage examples showing different integration patterns
- **`requirements.txt`** - Python package dependencies with version specifications

### Key Design Principles

1. **Single Responsibility**: Each module has one clear purpose
2. **Dependency Injection**: API keys can be provided or read from environment
3. **Lazy Loading**: Heavy resources initialized only when needed
4. **Error Resilience**: Automatic retries and graceful degradation
5. **Caching**: Smart caching to avoid redundant processing

## 🔧 Advanced Usage

### Custom Configuration

```python
from newsagent.core import NewsAPI

# Custom API instance
api = NewsAPI(
    news_api_key="custom_key",
    gemini_api_key="custom_key"
)

# Advanced processing
articles = api.get_daily_news(
    category="health",
    use_tiktok_summary=True,
    page_size=10,
    max_retries=15  # Higher retry count for better success rate
)
```

### Individual Service Usage

```python
from newsagent.services.processors import ArticleProcessor
from newsagent.services.ai_services import GeminiSummarizer

# Use individual services
processor = ArticleProcessor()
content = processor.extract_content("https://example.com/article")

summarizer = GeminiSummarizer(api_key="your_key")
summary = summarizer.generate_tiktok_summary(content.text)
```

### Error Handling

```python
from newsagent import get_daily_news
from newsagent.data.exceptions import NewsAPIError, ConfigurationError

try:
    articles = get_daily_news("business")
except ConfigurationError as e:
    print(f"Missing API keys: {e}")
except NewsAPIError as e:
    print(f"API error: {e}")
```

## 🧪 Testing

Run the example file to test all functionality:

```bash
python example.py
```

Or test the original API interface:

```bash
python api.py
```

## 📝 Logging

The package uses structured logging. Configure the logging level:

```python
import logging
logging.basicConfig(level=logging.DEBUG)  # For detailed logs
```

## 🔄 Migration from v1.0

The original `api.py` now serves as a compatibility layer. Existing code will continue to work:

```python
# Old way (still works)
from api import get_daily_news, NewsAPI

# New way (recommended)
from newsagent import get_daily_news, NewsAPIClient
```

## 🤝 Contributing

1. Follow PEP 8 style guidelines
2. Add docstrings to all public methods
3. Include type hints
4. Add appropriate logging
5. Update tests for new features

## 📄 License

This project is licensed under the MIT License.

## 🆘 Support

- Check the example.py file for usage patterns
- Enable debug logging for troubleshooting
- Review custom exceptions for specific error types