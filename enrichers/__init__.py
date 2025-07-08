"""
Data enrichment modules for Book Scraping Bot
"""

from .affiliate import AffiliateLinker
from .books_api import GoogleBooksEnricher
from .openlibrary import OpenLibraryEnricher

__all__ = [
    "AffiliateLinker",
    "GoogleBooksEnricher", 
    "OpenLibraryEnricher"
]