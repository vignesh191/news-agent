import os
import requests
from dotenv import load_dotenv
from newsapi import NewsApiClient

# Load variables from .env file
load_dotenv()
NEWS_API_KEY = os.getenv("NEWS_API_KEY")

# init newsapi client
newsapi = NewsApiClient(api_key=NEWS_API_KEY)

# /v2/top-headlines
top_headlines = newsapi.get_top_headlines(q='bitcoin',
                                          sources='bbc-news,the-verge',
                                          category='business',
                                          language='en',
                                          country='us')

# /v2/everything
all_articles = newsapi.get_everything(q='bitcoin',
                                      sources='bbc-news,the-verge',
                                      domains='bbc.co.uk,techcrunch.com',
                                      from_param='2017-12-01',
                                      to='2017-12-12',
                                      language='en',
                                      sort_by='relevancy',
                                      page=2)

# /v2/top-headlines/sources
sources = newsapi.get_sources()

# https://newsapi.org/docs/client-libraries/python

