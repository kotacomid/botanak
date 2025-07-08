"""
Content publishing modules for Book Scraping Bot
"""

from .static import StaticHTMLGenerator
from .wordpress import WordPressPublisher
from .blogspot import BlogspotPublisher

__all__ = [
    "StaticHTMLGenerator",
    "WordPressPublisher", 
    "BlogspotPublisher"
]