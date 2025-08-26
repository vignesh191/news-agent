# News Agent 📰✨

**Transform daily news into engaging content for any audience**

News Agent is a Python library that fetches top news headlines and creates AI-powered summaries optimized for different audiences. Whether you need general news summaries or TikTok-ready content for maximum engagement, News Agent delivers.

## 🎯 **What It Does**

- **📱 For TikTok Creators**: Get trendy, engaging summaries perfect for Gen-Z audiences and viral content
- **📊 For General Use**: Clean, professional news summaries for blogs, newsletters, or research
- **⚡ Automatic Processing**: Handles article extraction, AI summarization, and hashtag generation
- **🔄 Smart Retry Logic**: Never miss content due to failed downloads - automatically fetches backup articles

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

### 📱 **TikTok Content Creation**

```python
from client import get_daily_news

# Get 5 trending tech articles with TikTok-optimized summaries
articles = get_daily_news(
    category="technology",
    use_tiktok_summary=True,  # 🎯 Optimized for Gen-Z engagement
    page_size=5
)

for article in articles:
    print(f"🎬 Title: {article.title}")
    print(f"📝 Script: {article.summary}")  # Perfect for TikTok voiceover
    print(f"🏷️ Hashtags: {' '.join(article.hashtags[:5])}")
    print("---")
```

### 📊 **General News Summaries**

```python
from client import get_daily_news

# Get professional news summaries for business content
articles = get_daily_news(
    category="business",
    use_tiktok_summary=False,  # 📰 Standard professional summaries
    page_size=10
)

for article in articles:
    print(f"📰 {article.title}")
    print(f"📄 {article.summary}")
    print(f"🔗 Source: {article.source}")
```

## 📖 API Reference

### Main Functions

#### `get_daily_news(category, use_tiktok_summary, page_size, max_retries)`

**The main function you'll use 90% of the time.**

**Parameters:**
- `category` (str): News category - `"business"`, `"technology"`, `"sports"`, `"entertainment"`, `"health"`, `"science"`
- `use_tiktok_summary` (bool): 
  - `True` = TikTok-optimized summaries (trendy, engaging, Gen-Z friendly)
  - `False` = Professional summaries (clean, factual, business appropriate)
- `page_size` (int): Number of articles to get (default: 5)
- `max_retries` (int): Backup articles to try if some fail (default: 10)

**Returns:** List of `NewsArticle` objects with `.title`, `.summary`, `.hashtags`, `.source`, `.url`

### Classes

#### `NewsAgentClient`

Singleton-like client for reusable instances across your application.

```python
from news_agent.client import NewsAgentClient

client = NewsAgentClient.get_instance()
articles = client.get_daily_news("technology", page_size=3)
```

#### `NewsAgent`

Core class for advanced usage and custom configuration.

```python
from news_agent.core import NewsAgent

agent = NewsAgent(news_api_key="your_key", gemini_api_key="your_key")
articles = agent.get_daily_news("science", max_retries=20)
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

The package is organized into focused modules with a clean, flat structure:

```
news-agent/
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
├── utils/               # Utilities and configuration
│   ├── __init__.py      # Utils module exports
│   └── config.py        # Configuration constants and setup
├── requirements.txt     # Python package dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This documentation
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
- **`requirements.txt`** - Python package dependencies with version specifications
- **`.gitignore`** - Comprehensive ignore rules for Python projects
- **`README.md`** - Complete project documentation

### Key Design Principles

1. **Single Responsibility**: Each module has one clear purpose
2. **Dependency Injection**: API keys can be provided or read from environment
3. **Lazy Loading**: Heavy resources initialized only when needed
4. **Error Resilience**: Automatic retries and graceful degradation
5. **Caching**: Smart caching to avoid redundant processing

## 🔧 Advanced Usage

### 🔧 **Custom Configuration**

```python
from core import NewsAgent

# Custom API instance with your own keys
agent = NewsAgent(
    news_api_key="your_custom_key",
    gemini_api_key="your_custom_key"
)

# Advanced processing with higher success rate
articles = agent.get_daily_news(
    category="health",
    use_tiktok_summary=True,
    page_size=10,
    max_retries=20  # Try harder to get successful articles
)
```

### Individual Service Usage

```python
from services.processors import ArticleProcessor
from services.ai_services import GeminiSummarizer

# Use individual services
processor = ArticleProcessor()
content = processor.extract_content("https://example.com/article")

summarizer = GeminiSummarizer(api_key="your_key")
summary = summarizer.generate_tiktok_summary(content.text)
```

### Error Handling

```python
from client import get_daily_news
from data.exceptions import NewsAPIError, ConfigurationError

try:
    articles = get_daily_news("business")
except ConfigurationError as e:
    print(f"Missing API keys: {e}")
except NewsAPIError as e:
    print(f"API error: {e}")
```

## 🧪 Testing

Test the functionality directly:

```bash
python client.py
```

This will fetch business news with TikTok summaries and display the results.

## 🛠️ **Development Setup**

### **For Contributors**

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd news-agent
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Copy .env.example to .env and add your API keys
NEWS_API_KEY=your_newsapi_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

4. **Test the setup**
```bash
python client.py
```

### **Project Structure for Developers**

```
news-agent/
├── client.py              # 👤 Main user interface
├── core.py                # 🧠 Core business logic 
├── data/                  # 📊 Data models and exceptions
├── services/              # 🔧 External API integrations
├── utils/                 # 🛠️ Configuration and utilities
└── requirements.txt       # 📋 Dependencies
```

**Key Files to Understand:**
- **`client.py`** - Start here! Contains the main `get_daily_news()` function
- **`core.py`** - The orchestrator that coordinates all services
- **`services/`** - Individual services for news fetching, AI processing, content extraction
- **`utils/config.py`** - All configuration constants and settings

## 📝 Logging

The package uses structured logging. Configure the logging level:

```python
import logging
logging.basicConfig(level=logging.DEBUG)  # For detailed logs
```

## 🚀 Quick Start Examples

### Basic News Fetching
```python
from client import get_daily_news

# Get 5 technology articles
tech_news = get_daily_news("technology", page_size=5)
for article in tech_news:
    print(f"📰 {article.title}")
    print(f"📝 {article.summary}")
    print(f"🏷️ {' '.join(article.hashtags[:3])}")
    print("---")
```

### Advanced Configuration
```python
from news_agent.core import NewsAgent

# Initialize with custom settings
agent = NewsAgent()
sports_news = agent.get_daily_news(
    category="sports",
    use_tiktok_summary=True,
    page_size=10,
    max_retries=20
)
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