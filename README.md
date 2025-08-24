# News Agent - TikTok Content Generator

A Python API that fetches top news headlines, summarizes them using AI, and generates TikTok-ready content with hashtags.

## Features

- 📰 Fetch top 5 news headlines from NewsAPI for any category
- 🤖 AI-powered summaries using Google Gemini (TikTok-style) or newspaper3k NLP
- 🏷️ Automatic hashtag generation based on article keywords and category
- 📱 TikTok-ready content format with title, summary, source, date, and hashtags
- 🛡️ Robust error handling and fallback mechanisms

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd news-agent
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root with your API keys:
```env
NEWS_API_KEY=your_news_api_key_here
GEMINI_API_KEY=your_gemini_api_key_here
```

### Getting API Keys

- **NewsAPI Key**: Sign up at [newsapi.org](https://newsapi.org) (free tier available)
- **Gemini API Key**: Get from [Google AI Studio](https://makersuite.google.com/app/apikey)

## Usage

### Basic Usage

```python
from api import get_daily_news

# Get business news with TikTok-style summaries
news = get_daily_news(category="business", use_tiktok_summary=True)

# Get sports news with newspaper3k summaries
sports_news = get_daily_news(category="sports", use_tiktok_summary=False)
```

### Available Categories

- `business` - Business and financial news
- `sports` - Sports news and updates
- `technology` - Tech industry news
- `entertainment` - Entertainment and celebrity news
- `health` - Health and medical news
- `science` - Scientific discoveries and research
- `general` - General news and current events

### Response Format

The API returns a list of article dictionaries with the following structure:

```python
[
  {
    "title": "Article Title Here",
    "summary": "The generated summary/script here (TikTok-friendly or newspaper3k summary)",
    "source": "Website name or URL",
    "publishedAt": "2025-08-23T20:32:08Z",
    "hashtags": ["#Business", "#Finance", "#News"]
  }
]
```

### Example Output

```python
from api import get_daily_news

# Fetch technology news
tech_news = get_daily_news(category="technology", use_tiktok_summary=True)

for i, article in enumerate(tech_news, 1):
    print(f"\n{i}. {article['title']}")
    print(f"   Summary: {article['summary']}")
    print(f"   Source: {article['source']}")
    print(f"   Date: {article['publishedAt']}")
    print(f"   Hashtags: {' '.join(article['hashtags'])}")
```

**Example hashtags output:**
```
Hashtags: #technology #AI #innovation #startup #funding
```

## Advanced Usage

### Using the NewsAPI Class Directly

```python
from api import NewsAPI

# Create an instance
news_api = NewsAPI()

# Get raw headlines
headlines = news_api.get_top_headlines(category="business", page_size=10)

# Get article content with NLP
article_content = news_api.get_article_content("https://example.com/article")
if article_content:
    text, keywords, summary = article_content
    print(f"Keywords: {keywords}")
    print(f"NLP Summary: {summary}")

# Generate hashtags from URL
hashtags = news_api.generate_hashtags("https://example.com/article", "technology")
```

### Error Handling

The API includes robust error handling:

- If an article can't be fetched, it falls back to the description from NewsAPI
- If Gemini summarization fails, it uses newspaper3k summary
- If newspaper3k fails, it uses the article description
- Invalid URLs are skipped automatically
- NLTK data is automatically downloaded on first run

## TikTok Content Creation

This API is designed specifically for creating TikTok content:

1. **TikTok-Style Summaries**: When `use_tiktok_summary=True`, summaries are:
   - Conversational and engaging
   - Gen-Z friendly with trendy language
   - Optimized for reading aloud in videos
   - 3-4 sentences maximum

2. **Hashtag Strategy**: Hashtags are generated using:
   - **newspaper3k's NLP keywords** (automatically extracted and optimized)
   - Simply appends `#` to each keyword from `article.keywords`
   - No predefined hashtags - lets newspaper3k determine relevance

3. **Content Structure**: Each article provides:
   - **Title**: For video captions or text overlays
   - **Summary**: Script for voiceover or text-to-speech
   - **Source**: For attribution
   - **Date**: For timeliness context
   - **Hashtags**: For discoverability

## Testing

Run the built-in test:

```bash
python api.py
```

This will fetch business news with TikTok summaries and display the results.

## Dependencies

- `newsapi-python` - NewsAPI client
- `newspaper3k` - Article parsing and NLP
- `google-generativeai` - Gemini AI for summaries
- `python-dotenv` - Environment variable management
- `nltk` - Natural language processing (automatically downloaded)

## Troubleshooting

### Common Issues

1. **API Key Errors**: Ensure your `.env` file contains valid API keys
2. **Network Issues**: Some articles may fail to fetch due to paywalls or blocking
3. **Rate Limits**: NewsAPI has rate limits on free tier
4. **Gemini Errors**: Check your Gemini API key and quota
5. **NLTK Download**: First run will download required NLTK data automatically

### Debug Mode

For debugging, you can create a NewsAPI instance directly:

```python
from api import NewsAPI

news_api = NewsAPI()
# This will show detailed error messages
```

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues and enhancement requests!
