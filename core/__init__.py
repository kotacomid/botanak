"""
Core modules for Book Scraping Bot
"""

from .scraper import BookScraper, AnnasArchiveScraper, LibGenScraper
from .metadata import MetadataProcessor, BookMetadata
from .downloader import FileDownloader

__all__ = [
    "BookScraper", 
    "AnnasArchiveScraper", 
    "LibGenScraper",
    "MetadataProcessor", 
    "BookMetadata",
    "FileDownloader"
]