import os
from typing import List, Dict, Optional, Tuple
from dotenv import load_dotenv
from newsapi import NewsApiClient
from newspaper import Article
from google import genai
import nltk
nltk.download('punkt_tab')

# Load environment variables
load_dotenv()

class NewsAPI:
    # Clean API for fetching and summarizing news articles for TikTok content creation
    
    def __init__(self):
        # Initialize with required API keys
        self.news_api_key = os.getenv("NEWS_API_KEY")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        
        if not self.news_api_key:
            raise ValueError("NEWS_API_KEY environment variable is required")
        if not self.gemini_api_key:
            raise ValueError("GEMINI_API_KEY environment variable is required")
        
        # Initialize clients
        self.newsapi = NewsApiClient(api_key=self.news_api_key)
        self.gemini_client = genai.Client(api_key=self.gemini_api_key)
    
    def get_top_headlines(self, category: str, page_size: int = 5) -> List[Dict]:
        # Fetch top headlines from NewsAPI for a given category
        try:
            response = self.newsapi.get_top_headlines(
                language='en',
                country='us',
                page_size=page_size,
                category=category
            )
            return response.get('articles', [])
        except Exception as e:
            print(f"Error fetching headlines for category '{category}': {e}")
            return []
    
    def get_article_content(self, url: str) -> Optional[Tuple[str, List[str], str]]:
        # Fetch and parse article content using newspaper3k
        try:
            article = Article(url)
            article.download()
            article.parse()
            article.nlp()  # Extract keywords and summary
            return article.text, article.keywords, article.summary
        except Exception as e:
            print(f"Failed to fetch article from {url}: {e}")
            return None
    
    def generate_tiktok_summary(self, text: str) -> str:
        # Generate TikTok-style summary using Gemini
        if not text:
            return "No content available"
        
        prompt = f"""
        You are a TikTok content creator targeting a Gen-Z audience. 
        Summarize the following news article in 3–4 trendy and easy-to-understand sentences. 
        - Make it fun and conversational, with a touch of witty humor. 
        - Keep the audience engaged; views are the goal. 
        - Focus on the main points and avoid unnecessary details. 
        - The summary should be suitable for reading aloud in a TikTok video.
        - Do not use any hashtags.

        Article:
        {text[:3000]}  # Limit text length to avoid token limits
        """
        
        try:
            response = self.gemini_client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=prompt
            )
            return response.text.strip()
        except Exception as e:
            print(f"Error generating TikTok summary: {e}")
            return "Summary generation failed"
    
    def generate_hashtags(self, url: str, category: str) -> List[str]:
        # Get article content and use newspaper3k keywords as hashtags
        hashtags = []
        
        article_content = self.get_article_content(url)
        if article_content:
            text, keywords, summary = article_content
            if keywords:
                for keyword in keywords:
                    hashtags.append(f"#{keyword}")
        
        return hashtags
    
    def get_daily_news(self, category: str = "business", use_tiktok_summary: bool = True) -> List[Dict]:
        # Main API method to get daily news articles with summaries and hashtags
        articles_data = []
        
        # Fetch top headlines
        headlines = self.get_top_headlines(category)
        
        if not headlines:
            print(f"No headlines found for category: {category}")
            return []
        
        for article in headlines:
            try:
                # Extract basic info
                title = article.get('title', 'No title available')
                source = article.get('source', {}).get('name', 'Unknown source')
                published_at = article.get('publishedAt', '')
                url = article.get('url', '')
                
                if not url:
                    continue
                
                # Fetch full article content using newspaper3k
                parsed_article = self.get_article_content(url)
                
                if not parsed_article:
                    summary = article.get('description', 'No summary available')
                else:
                    text, keywords, nlp_summary = parsed_article
                    if use_tiktok_summary:
                        summary = self.generate_tiktok_summary(text)
                    else:
                        summary = nlp_summary or 'No summary available'
                
                hashtags = self.generate_hashtags(url, category)
                
                article_data = {
                    "title": title,
                    "summary": summary,
                    "source": source,
                    "publishedAt": published_at,
                    "hashtags": hashtags
                }
                
                articles_data.append(article_data)
                
            except Exception as e:
                print(f"Error processing article '{title}': {e}")
                continue
        
        return articles_data

# Create a global instance for easy access
_news_api = None

def get_daily_news(category: str = "business", use_tiktok_summary: bool = True) -> List[Dict]:
    # Convenience function to get daily news articles
    global _news_api
    if _news_api is None:
        _news_api = NewsAPI()
    
    return _news_api.get_daily_news(category, use_tiktok_summary)

# Test the API
if __name__ == "__main__":
    try:
        print("Fetching business news with TikTok summaries...")
        news = get_daily_news(category="business", use_tiktok_summary=True)
        
        print(f"Found {len(news)} articles:")
        for i, article in enumerate(news, 1):
            print(f"\n{i}. {article['title']}")
            print(f"   Summary: {article['summary']}")
            print(f"   Source: {article['source']}")
            print(f"   Hashtags: {' '.join(article['hashtags'])}")
        
    except Exception as e:
        print(f"Error testing API: {e}")

