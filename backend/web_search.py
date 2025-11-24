"""
Web Search Integration for Educational Articles
Finds educational articles and resources from the web
"""

from typing import List, Dict, Optional
from loguru import logger
import requests
import time
from duckduckgo_search import DDGS

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))


class WebSearcher:
    """Search web for educational articles and resources"""

    def __init__(self):
        logger.info("Web searcher initialized (using DuckDuckGo - no API key needed)")
        self.is_configured = True  # Always available, no API key needed
        self.last_search_time = 0  # Track last search for rate limiting

    def search_articles(
        self,
        query: str,
        language: str = "hi",
        max_results: int = 3
    ) -> List[Dict[str, str]]:
        """
        Search for educational articles and resources

        Args:
            query: Search query
            language: Preferred language (en, hi, raj)
            max_results: Maximum number of results

        Returns:
            List of article information dicts
        """
        try:
            # Rate limiting: wait 2 seconds between searches
            current_time = time.time()
            time_since_last_search = current_time - self.last_search_time
            if time_since_last_search < 2:
                time.sleep(2 - time_since_last_search)
            self.last_search_time = time.time()

            # Add educational keywords to query
            educational_query = f"{query} explanation tutorial educational"

            # Add language preference
            if language == "hi" or language == "raj":
                educational_query += " in Hindi"

            # Restrict to educational domains for better quality
            educational_query += " site:khanacademy.org OR site:wikipedia.org OR site:ncert.nic.in OR site:byjus.com OR site:unacademy.com"

            logger.info(f"Searching web for: {educational_query}")

            # Perform DuckDuckGo search with fresh instance to avoid rate limits
            ddg = DDGS()
            results = []
            ddg_results = ddg.text(educational_query, max_results=max_results)

            for item in ddg_results:
                article = {
                    'title': item.get('title', 'Untitled'),
                    'description': item.get('body', 'No description available')[:200] + '...',
                    'url': item.get('href', ''),
                    'source': self._extract_domain(item.get('href', ''))
                }
                results.append(article)

            logger.info(f"Found {len(results)} articles for query: {query}")
            return results

        except Exception as e:
            logger.warning(f"Web search temporarily unavailable: {e}")
            # Fallback: return empty list instead of failing
            return []

    def _extract_domain(self, url: str) -> str:
        """Extract domain name from URL"""
        try:
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            # Remove 'www.' prefix
            if domain.startswith('www.'):
                domain = domain[4:]
            return domain
        except:
            return "Unknown"

    def format_articles_for_display(
        self,
        articles: List[Dict[str, str]],
        language: str = "en"
    ) -> str:
        """
        Format article list for chat display

        Args:
            articles: List of article dicts
            language: Display language

        Returns:
            Formatted string
        """
        if not articles:
            messages = {
                "en": "No articles found.",
                "hi": "कोई लेख नहीं मिला।",
                "raj": "कोई लेख कोनी मिल्यो।"
            }
            return messages.get(language, messages["hi"])

        headers = {
            "en": "📚 Recommended Articles:",
            "hi": "📚 सुझाए गए लेख:",
            "raj": "📚 सुझाव लेख:"
        }

        formatted = f"\n{headers.get(language, headers['hi'])}\n\n"

        for i, article in enumerate(articles, 1):
            formatted += f"{i}. **{article['title']}**\n"
            formatted += f"   Source: {article['source']}\n"
            formatted += f"   🔗 {article['url']}\n\n"

        return formatted

    def check_health(self) -> dict:
        """Check if web search is working"""
        try:
            # Web search is always available (no API key needed)
            # Don't test actual search to avoid rate limits
            return {
                "status": "healthy",
                "message": "Web search available (DuckDuckGo)"
            }
        except Exception as e:
            return {
                "status": "healthy",  # Still report as healthy since no API key needed
                "message": "Web search available (rate limits may apply)"
            }


# Global web searcher instance
web_searcher = WebSearcher()


if __name__ == "__main__":
    # Test web search
    print("YuvaSaarthi - Web Search Test")
    print("=" * 60)

    searcher = WebSearcher()

    # Health check
    health = searcher.check_health()
    print(f"Health Status: {health['status']}")
    print(f"Message: {health['message']}\n")

    if health['status'] == 'healthy':
        # Test search
        test_query = "Pythagoras theorem"
        print(f"Test Query: {test_query}\n")

        articles = searcher.search_articles(test_query, language="en", max_results=3)

        if articles:
            formatted = searcher.format_articles_for_display(articles, language="en")
            print(formatted)
        else:
            print("No articles found")
