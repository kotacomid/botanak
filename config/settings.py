"""
Book Scraping Bot Configuration
Supports both Free and Paid tier features
"""

import os
from typing import Dict, List, Optional


class Settings:
    """Main configuration class for the book scraping bot"""
    
    def __init__(self):
        # App Configuration
        self.APP_NAME = "Book Scraping Bot"
        self.VERSION = "1.0.0"
        self.DEBUG = self._get_bool_env("DEBUG", False)
        
        # Tier Configuration
        self.IS_PREMIUM = self._get_bool_env("IS_PREMIUM", False)
        
        # Scraping Configuration
        self.SCRAPING_DELAY = self._get_float_env("SCRAPING_DELAY", 1.0)
        self.MAX_RETRIES = self._get_int_env("MAX_RETRIES", 3)
        self.TIMEOUT = self._get_int_env("TIMEOUT", 30)
        self.USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
        
        # Sources Configuration
        self.ANNAS_ARCHIVE_URL = "https://annas-archive.org"
        self.LIBGEN_URLS = [
            "https://libgen.rs",
            "https://libgen.li", 
            "https://libgen.is"
        ]
        
        # Output Configuration
        self.OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
        self.CLEAN_FILENAME = True
        self.SAVE_METADATA_JSON = True
        self.SAVE_METADATA_CSV = True
        self.GENERATE_HTML = True
        
        # Download Configuration
        self.DOWNLOAD_BOOKS = self._get_bool_env("DOWNLOAD_BOOKS", True)
        self.DOWNLOAD_COVERS = self._get_bool_env("DOWNLOAD_COVERS", True)
        self.MAX_FILE_SIZE_MB = self._get_int_env("MAX_FILE_SIZE_MB", 100)
        
        # Google Drive Configuration
        self.GDRIVE_ENABLED = self._get_bool_env("GDRIVE_ENABLED", False)
        self.GDRIVE_FOLDER_ID = os.getenv("GDRIVE_FOLDER_ID")
        self.GDRIVE_CREDENTIALS_FILE = "config/gdrive_credentials.json"
        self.GDRIVE_TOKEN_FILE = "config/gdrive_token.json"
        
        # FTP Configuration
        self.FTP_ENABLED = self._get_bool_env("FTP_ENABLED", False)
        self.FTP_HOST = os.getenv("FTP_HOST")
        self.FTP_PORT = self._get_int_env("FTP_PORT", 21)
        self.FTP_USERNAME = os.getenv("FTP_USERNAME")
        self.FTP_PASSWORD = os.getenv("FTP_PASSWORD")
        self.FTP_DIRECTORY = os.getenv("FTP_DIRECTORY", "/")
        
        # API Keys for Data Enrichment
        self.GOOGLE_BOOKS_API_KEY = os.getenv("GOOGLE_BOOKS_API_KEY")
        self.OPENLIBRARY_API_URL = "https://openlibrary.org/api"
        
        # Affiliate Configuration
        self.AMAZON_AFFILIATE_TAG = os.getenv("AMAZON_AFFILIATE_TAG")
        self.EBAY_AFFILIATE_ID = os.getenv("EBAY_AFFILIATE_ID")
        
        # WordPress Configuration
        self.WORDPRESS_ENABLED = self._get_bool_env("WORDPRESS_ENABLED", False)
        self.WORDPRESS_URL = os.getenv("WORDPRESS_URL")
        self.WORDPRESS_USERNAME = os.getenv("WORDPRESS_USERNAME")
        self.WORDPRESS_PASSWORD = os.getenv("WORDPRESS_PASSWORD")
        
        # Blogspot Configuration
        self.BLOGSPOT_ENABLED = self._get_bool_env("BLOGSPOT_ENABLED", False)
        self.BLOGSPOT_BLOG_ID = os.getenv("BLOGSPOT_BLOG_ID")
        self.BLOGSPOT_API_KEY = os.getenv("BLOGSPOT_API_KEY")
        
        # Premium Features (Paid Tier)
        self.VIDEO_GENERATION_ENABLED = self._get_bool_env("VIDEO_GENERATION_ENABLED", False)
        self.TELEGRAM_BOT_ENABLED = self._get_bool_env("TELEGRAM_BOT_ENABLED", False)
        self.TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
        self.TELEGRAM_CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")
        
        # Analytics (Premium)
        self.ANALYTICS_ENABLED = self._get_bool_env("ANALYTICS_ENABLED", False)
        self.ANALYTICS_DB_PATH = "data/analytics.db"
        
        # Video Generation Settings (Premium)
        self.VIDEO_WIDTH = 1080
        self.VIDEO_HEIGHT = 1920  # Vertical for TikTok/Reels
        self.VIDEO_FPS = 30
        self.TTS_LANGUAGE = "en"
        
        # Rate Limiting
        self.REQUESTS_PER_MINUTE = self._get_int_env("REQUESTS_PER_MINUTE", 60)
        self.PREMIUM_REQUESTS_PER_MINUTE = self._get_int_env("PREMIUM_REQUESTS_PER_MINUTE", 300)
    
    def _get_bool_env(self, key: str, default: bool) -> bool:
        """Get boolean environment variable"""
        value = os.getenv(key, str(default)).lower()
        return value in ('true', '1', 'yes', 'on')
    
    def _get_int_env(self, key: str, default: int) -> int:
        """Get integer environment variable"""
        try:
            return int(os.getenv(key, str(default)))
        except (ValueError, TypeError):
            return default
    
    def _get_float_env(self, key: str, default: float) -> float:
        """Get float environment variable"""
        try:
            return float(os.getenv(key, str(default)))
        except (ValueError, TypeError):
            return default
    
    @property
    def requests_per_minute(self) -> int:
        """Get appropriate rate limit based on tier"""
        return self.PREMIUM_REQUESTS_PER_MINUTE if self.IS_PREMIUM else self.REQUESTS_PER_MINUTE
    
    @property
    def max_concurrent_downloads(self) -> int:
        """Get max concurrent downloads based on tier"""
        return 10 if self.IS_PREMIUM else 3
    
    def get_enabled_features(self) -> Dict[str, bool]:
        """Get all enabled features for current tier"""
        features = {
            "metadata_scraping": True,
            "file_download": self.DOWNLOAD_BOOKS,
            "cover_download": self.DOWNLOAD_COVERS,
            "gdrive_upload": self.GDRIVE_ENABLED,
            "ftp_upload": self.FTP_ENABLED,
            "wordpress_posting": self.WORDPRESS_ENABLED,
            "blogspot_posting": self.BLOGSPOT_ENABLED,
            "html_generation": self.GENERATE_HTML,
        }
        
        # Premium features
        if self.IS_PREMIUM:
            features.update({
                "video_generation": self.VIDEO_GENERATION_ENABLED,
                "telegram_notifications": self.TELEGRAM_BOT_ENABLED,
                "advanced_analytics": self.ANALYTICS_ENABLED,
                "unlimited_downloads": True,
                "priority_support": True,
            })
        
        return features


# Create global settings instance
settings = Settings()


def validate_config() -> List[str]:
    """Validate configuration and warn about missing settings"""
    warnings = []
    
    if settings.GDRIVE_ENABLED and not settings.GDRIVE_FOLDER_ID:
        warnings.append("Google Drive enabled but no folder ID provided")
    
    if settings.FTP_ENABLED and not all([settings.FTP_HOST, settings.FTP_USERNAME]):
        warnings.append("FTP enabled but credentials incomplete")
    
    if settings.WORDPRESS_ENABLED and not all([settings.WORDPRESS_URL, settings.WORDPRESS_USERNAME]):
        warnings.append("WordPress enabled but credentials incomplete")
    
    # Premium feature warnings
    if settings.IS_PREMIUM:
        if settings.VIDEO_GENERATION_ENABLED and not settings.TTS_LANGUAGE:
            warnings.append("Video generation enabled but no TTS language set")
        
        if settings.TELEGRAM_BOT_ENABLED and not settings.TELEGRAM_BOT_TOKEN:
            warnings.append("Telegram bot enabled but no token provided")
    
    return warnings