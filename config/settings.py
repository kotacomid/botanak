"""
Book Scraping Bot Configuration
Supports both Free and Paid tier features
"""

import os
from typing import Dict, List, Optional
from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Main configuration class for the book scraping bot"""
    
    # App Configuration
    APP_NAME: str = "Book Scraping Bot"
    VERSION: str = "1.0.0"
    DEBUG: bool = Field(default=False, env="DEBUG")
    
    # Tier Configuration
    IS_PREMIUM: bool = Field(default=False, env="IS_PREMIUM")
    
    # Scraping Configuration
    SCRAPING_DELAY: float = Field(default=1.0, env="SCRAPING_DELAY")
    MAX_RETRIES: int = Field(default=3, env="MAX_RETRIES")
    TIMEOUT: int = Field(default=30, env="TIMEOUT")
    USER_AGENT: str = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"
    
    # Sources Configuration
    ANNAS_ARCHIVE_URL: str = "https://annas-archive.org"
    LIBGEN_URLS: List[str] = [
        "https://libgen.rs",
        "https://libgen.li", 
        "https://libgen.is"
    ]
    
    # Output Configuration
    OUTPUT_DIR: str = Field(default="output", env="OUTPUT_DIR")
    CLEAN_FILENAME: bool = True
    SAVE_METADATA_JSON: bool = True
    SAVE_METADATA_CSV: bool = True
    GENERATE_HTML: bool = True
    
    # Download Configuration
    DOWNLOAD_BOOKS: bool = Field(default=True, env="DOWNLOAD_BOOKS")
    DOWNLOAD_COVERS: bool = Field(default=True, env="DOWNLOAD_COVERS")
    MAX_FILE_SIZE_MB: int = Field(default=100, env="MAX_FILE_SIZE_MB")
    
    # Google Drive Configuration
    GDRIVE_ENABLED: bool = Field(default=False, env="GDRIVE_ENABLED")
    GDRIVE_FOLDER_ID: Optional[str] = Field(default=None, env="GDRIVE_FOLDER_ID")
    GDRIVE_CREDENTIALS_FILE: str = "config/gdrive_credentials.json"
    GDRIVE_TOKEN_FILE: str = "config/gdrive_token.json"
    
    # FTP Configuration
    FTP_ENABLED: bool = Field(default=False, env="FTP_ENABLED")
    FTP_HOST: Optional[str] = Field(default=None, env="FTP_HOST")
    FTP_PORT: int = Field(default=21, env="FTP_PORT")
    FTP_USERNAME: Optional[str] = Field(default=None, env="FTP_USERNAME")
    FTP_PASSWORD: Optional[str] = Field(default=None, env="FTP_PASSWORD")
    FTP_DIRECTORY: str = Field(default="/", env="FTP_DIRECTORY")
    
    # API Keys for Data Enrichment
    GOOGLE_BOOKS_API_KEY: Optional[str] = Field(default=None, env="GOOGLE_BOOKS_API_KEY")
    OPENLIBRARY_API_URL: str = "https://openlibrary.org/api"
    
    # Affiliate Configuration
    AMAZON_AFFILIATE_TAG: Optional[str] = Field(default=None, env="AMAZON_AFFILIATE_TAG")
    EBAY_AFFILIATE_ID: Optional[str] = Field(default=None, env="EBAY_AFFILIATE_ID")
    
    # WordPress Configuration
    WORDPRESS_ENABLED: bool = Field(default=False, env="WORDPRESS_ENABLED")
    WORDPRESS_URL: Optional[str] = Field(default=None, env="WORDPRESS_URL")
    WORDPRESS_USERNAME: Optional[str] = Field(default=None, env="WORDPRESS_USERNAME")
    WORDPRESS_PASSWORD: Optional[str] = Field(default=None, env="WORDPRESS_PASSWORD")
    
    # Blogspot Configuration
    BLOGSPOT_ENABLED: bool = Field(default=False, env="BLOGSPOT_ENABLED")
    BLOGSPOT_BLOG_ID: Optional[str] = Field(default=None, env="BLOGSPOT_BLOG_ID")
    BLOGSPOT_API_KEY: Optional[str] = Field(default=None, env="BLOGSPOT_API_KEY")
    
    # Premium Features (Paid Tier)
    VIDEO_GENERATION_ENABLED: bool = Field(default=False, env="VIDEO_GENERATION_ENABLED")
    TELEGRAM_BOT_ENABLED: bool = Field(default=False, env="TELEGRAM_BOT_ENABLED")
    TELEGRAM_BOT_TOKEN: Optional[str] = Field(default=None, env="TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHANNEL_ID: Optional[str] = Field(default=None, env="TELEGRAM_CHANNEL_ID")
    
    # Analytics (Premium)
    ANALYTICS_ENABLED: bool = Field(default=False, env="ANALYTICS_ENABLED")
    ANALYTICS_DB_PATH: str = "data/analytics.db"
    
    # Video Generation Settings (Premium)
    VIDEO_WIDTH: int = 1080
    VIDEO_HEIGHT: int = 1920  # Vertical for TikTok/Reels
    VIDEO_FPS: int = 30
    TTS_LANGUAGE: str = "en"
    
    # Rate Limiting
    REQUESTS_PER_MINUTE: int = Field(default=60, env="REQUESTS_PER_MINUTE")
    PREMIUM_REQUESTS_PER_MINUTE: int = Field(default=300, env="PREMIUM_REQUESTS_PER_MINUTE")
    
    class Config:
        env_file = ".env"
        case_sensitive = True
    
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

# Validation
def validate_config():
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