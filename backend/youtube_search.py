"""
YouTube Video Search Integration
Finds educational videos relevant to queries
"""

from typing import List, Dict, Optional
from googleapiclient.discovery import build
from loguru import logger

import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import settings


class YouTubeSearcher:
    """Search YouTube for educational videos"""

    def __init__(self):
        self.api_key = settings.youtube_api_key
        self.is_configured = bool(
            self.api_key and
            self.api_key != "your_youtube_api_key"
        )

        if self.is_configured:
            try:
                self.youtube = build('youtube', 'v3', developerKey=self.api_key)
                logger.info("YouTube API initialized")
            except Exception as e:
                logger.error(f"YouTube API initialization failed: {e}")
                self.youtube = None
                self.is_configured = False
        else:
            self.youtube = None
            logger.warning("YouTube API key not configured")

    def search_videos(
        self,
        query: str,
        language: str = "hi",
        max_results: int = 3
    ) -> List[Dict[str, str]]:
        """
        Search for educational videos

        Args:
            query: Search query
            language: Preferred language (en, hi, raj)
            max_results: Maximum number of results

        Returns:
            List of video information dicts
        """
        if not self.is_configured or not self.youtube:
            logger.warning("YouTube search not available")
            return []

        try:
            # Add educational keywords to query
            educational_query = f"{query} tutorial explanation in {self._get_language_name(language)}"

            # Search parameters
            search_params = {
                'q': educational_query,
                'part': 'snippet',
                'maxResults': 10,  # Fetch more to filter
                'type': 'video',
                'videoCategoryId': '27',  # Education category
                'videoDuration': 'medium',  # Exclude shorts (4-20 mins)
                'videoEmbeddable': 'true',
                'safeSearch': 'strict',
                'relevanceLanguage': self._get_youtube_language_code(language),
                'order': 'relevance'
            }

            # Execute search
            response = self.youtube.search().list(**search_params).execute()

            # Parse results
            videos = []
            for item in response.get('items', []):
                title = item['snippet']['title']
                # Extra safety: Exclude shorts if they slip through
                if '#shorts' in title.lower() or 'short' in title.lower():
                    continue

                video = {
                    'title': title,
                    'description': item['snippet']['description'][:150] + '...',
                    'video_id': item['id']['videoId'],
                    'url': f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                    'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                    'channel': item['snippet']['channelTitle']
                }
                videos.append(video)
                
                if len(videos) >= max_results:
                    break

            logger.info(f"Found {len(videos)} videos for query: {query}")
            return videos

        except Exception as e:
            logger.error(f"YouTube search error: {e}")
            return []

    def _get_language_name(self, code: str) -> str:
        """Get full language name for search query"""
        names = {
            "en": "English",
            "hi": "Hindi",
            "raj": "Hindi"  # Use Hindi for Rajasthani
        }
        return names.get(code, "Hindi")

    def _get_youtube_language_code(self, code: str) -> str:
        """Get YouTube API language code"""
        codes = {
            "en": "en",
            "hi": "hi",
            "raj": "hi"
        }
        return codes.get(code, "hi")

    def format_videos_for_display(self, videos: List[Dict[str, str]], language: str = "en") -> str:
        """
        Format video list for chat display

        Args:
            videos: List of video dicts
            language: Display language

        Returns:
            Formatted string
        """
        if not videos:
            messages = {
                "en": "No videos found.",
                "hi": "कोई वीडियो नहीं मिला।",
                "raj": "कोई वीडियो कोनी मिल्यो।"
            }
            return messages.get(language, messages["hi"])

        headers = {
            "en": "📺 Recommended Videos:",
            "hi": "📺 सुझाए गए वीडियो:",
            "raj": "📺 सुझाव वीडियो:"
        }

        formatted = f"\n{headers.get(language, headers['hi'])}\n\n"

        for i, video in enumerate(videos, 1):
            formatted += f"{i}. [{video['title']}]({video['url']})\n"
            formatted += f"   Channel: {video['channel']}\n\n"

        return formatted

    def check_health(self) -> dict:
        """Check if YouTube API is working"""
        if not self.is_configured:
            return {
                "status": "not_configured",
                "message": "YouTube API key not configured"
            }

        try:
            # Try a simple search
            response = self.youtube.search().list(
                q='test',
                part='snippet',
                maxResults=1
            ).execute()

            return {
                "status": "healthy",
                "message": "YouTube API is working"
            }

        except Exception as e:
            return {
                "status": "error",
                "message": str(e)
            }


# Global YouTube searcher instance
youtube_searcher = YouTubeSearcher()


if __name__ == "__main__":
    # Test YouTube search
    print("YuvaSaarthi - YouTube Search Test")
    print("=" * 60)

    searcher = YouTubeSearcher()

    # Health check
    health = searcher.check_health()
    print(f"Health Status: {health['status']}")
    print(f"Message: {health['message']}\n")

    if health['status'] == 'healthy':
        # Test search
        test_query = "Pythagoras theorem"
        print(f"Test Query: {test_query}\n")

        videos = searcher.search_videos(test_query, language="hi", max_results=3)

        if videos:
            formatted = searcher.format_videos_for_display(videos, language="en")
            print(formatted)
        else:
            print("No videos found")
