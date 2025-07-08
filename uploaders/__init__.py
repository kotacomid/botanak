"""
Upload modules for Book Scraping Bot
"""

from .gdrive import GoogleDriveUploader
from .ftp import FTPUploader

__all__ = [
    "GoogleDriveUploader",
    "FTPUploader"
]