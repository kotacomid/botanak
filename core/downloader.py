"""
File Download Module
Handles downloading of book files and cover images
"""

import os
import requests
import asyncio
import aiohttp
import hashlib
from pathlib import Path
from typing import Optional, Dict, List
from urllib.parse import urlparse, unquote
import logging
from concurrent.futures import ThreadPoolExecutor

from config.settings import settings
from .metadata import BookMetadata

logger = logging.getLogger(__name__)


class FileDownloader:
    """Handle file downloads with progress tracking and error handling"""
    
    def __init__(self, output_dir: str = None):
        self.output_dir = Path(output_dir or settings.OUTPUT_DIR)
        self.books_dir = self.output_dir / "books"
        self.covers_dir = self.output_dir / "covers"
        
        # Create directories
        self.books_dir.mkdir(parents=True, exist_ok=True)
        self.covers_dir.mkdir(parents=True, exist_ok=True)
        
        # Session for downloads
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': settings.USER_AGENT,
            'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def download_book(self, metadata: BookMetadata) -> Optional[str]:
        """Download book file and return local path"""
        if not metadata.download_url:
            logger.warning(f"No download URL for book: {metadata.title}")
            return None
        
        try:
            # Determine filename
            filename = self._get_book_filename(metadata)
            filepath = self.books_dir / filename
            
            # Skip if already exists
            if filepath.exists():
                logger.info(f"Book already exists: {filename}")
                return str(filepath)
            
            # Download file
            success = self._download_file(metadata.download_url, filepath)
            
            if success:
                # Verify file
                if self._verify_book_file(filepath):
                    logger.info(f"Successfully downloaded book: {filename}")
                    return str(filepath)
                else:
                    logger.warning(f"Downloaded file appears corrupted: {filename}")
                    filepath.unlink(missing_ok=True)
                    return None
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error downloading book {metadata.title}: {e}")
            return None
    
    def download_cover(self, metadata: BookMetadata) -> Optional[str]:
        """Download cover image and return local path"""
        if not metadata.cover_url:
            logger.warning(f"No cover URL for book: {metadata.title}")
            return None
        
        try:
            # Determine filename
            filename = self._get_cover_filename(metadata)
            filepath = self.covers_dir / filename
            
            # Skip if already exists
            if filepath.exists():
                logger.info(f"Cover already exists: {filename}")
                return str(filepath)
            
            # Download cover
            success = self._download_file(metadata.cover_url, filepath)
            
            if success:
                logger.info(f"Successfully downloaded cover: {filename}")
                return str(filepath)
            else:
                return None
                
        except Exception as e:
            logger.error(f"Error downloading cover for {metadata.title}: {e}")
            return None
    
    def _download_file(self, url: str, filepath: Path) -> bool:
        """Download file with progress tracking"""
        try:
            logger.info(f"Downloading: {url}")
            
            response = self.session.get(url, stream=True, timeout=settings.TIMEOUT)
            response.raise_for_status()
            
            # Check file size
            content_length = response.headers.get('content-length')
            if content_length:
                file_size_mb = int(content_length) / (1024 * 1024)
                if file_size_mb > settings.MAX_FILE_SIZE_MB:
                    logger.warning(f"File too large: {file_size_mb:.1f}MB > {settings.MAX_FILE_SIZE_MB}MB")
                    return False
            
            # Download with progress
            with open(filepath, 'wb') as f:
                downloaded = 0
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        # Log progress for large files
                        if content_length and downloaded % (1024 * 1024) == 0:
                            progress = (downloaded / int(content_length)) * 100
                            logger.debug(f"Download progress: {progress:.1f}%")
            
            return True
            
        except requests.RequestException as e:
            logger.error(f"Download failed: {e}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error during download: {e}")
            return False
    
    def _get_book_filename(self, metadata: BookMetadata) -> str:
        """Generate filename for book file"""
        base_name = metadata.filename_base
        extension = self._get_file_extension(metadata.file_format or "pdf")
        return f"{base_name}.{extension}"
    
    def _get_cover_filename(self, metadata: BookMetadata) -> str:
        """Generate filename for cover image"""
        base_name = metadata.filename_base
        # Try to get extension from URL, default to jpg
        extension = self._get_image_extension(metadata.cover_url)
        return f"{base_name}.{extension}"
    
    def _get_file_extension(self, file_format: str) -> str:
        """Get appropriate file extension"""
        format_map = {
            'PDF': 'pdf',
            'EPUB': 'epub',
            'MOBI': 'mobi',
            'AZW3': 'azw3',
            'TXT': 'txt',
            'RTF': 'rtf',
            'DOC': 'doc',
            'DOCX': 'docx',
        }
        return format_map.get(file_format.upper(), 'pdf')
    
    def _get_image_extension(self, url: str) -> str:
        """Extract image extension from URL"""
        if not url:
            return 'jpg'
        
        parsed = urlparse(url)
        path = unquote(parsed.path.lower())
        
        for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            if path.endswith(ext):
                return ext[1:]  # Remove the dot
        
        return 'jpg'  # Default
    
    def _verify_book_file(self, filepath: Path) -> bool:
        """Verify downloaded book file is valid"""
        if not filepath.exists():
            return False
        
        # Check file size
        file_size = filepath.stat().st_size
        if file_size < 1024:  # Less than 1KB is suspicious
            return False
        
        # Check file format based on extension
        extension = filepath.suffix.lower()
        
        if extension == '.pdf':
            return self._verify_pdf(filepath)
        elif extension in ['.epub', '.mobi', '.azw3']:
            return self._verify_ebook(filepath)
        else:
            return True  # Assume other formats are OK if size is reasonable
    
    def _verify_pdf(self, filepath: Path) -> bool:
        """Verify PDF file"""
        try:
            with open(filepath, 'rb') as f:
                header = f.read(8)
                return header.startswith(b'%PDF-')
        except Exception:
            return False
    
    def _verify_ebook(self, filepath: Path) -> bool:
        """Verify ebook file (EPUB, MOBI, etc.)"""
        try:
            # Basic size check
            file_size = filepath.stat().st_size
            return file_size > 10240  # Greater than 10KB
        except Exception:
            return False
    
    def calculate_file_hash(self, filepath: Path) -> str:
        """Calculate MD5 hash of file"""
        try:
            hash_md5 = hashlib.md5()
            with open(filepath, "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logger.error(f"Error calculating hash for {filepath}: {e}")
            return ""
    
    async def download_multiple_async(self, metadata_list: List[BookMetadata]) -> Dict[str, str]:
        """Download multiple files asynchronously"""
        results = {}
        
        # Limit concurrent downloads based on tier
        semaphore = asyncio.Semaphore(settings.max_concurrent_downloads)
        
        async def download_single(metadata: BookMetadata):
            async with semaphore:
                book_path = None
                cover_path = None
                
                if settings.DOWNLOAD_BOOKS and metadata.download_url:
                    book_path = await self._download_async(metadata.download_url, 
                                                         self._get_book_filename(metadata), 
                                                         self.books_dir)
                
                if settings.DOWNLOAD_COVERS and metadata.cover_url:
                    cover_path = await self._download_async(metadata.cover_url,
                                                          self._get_cover_filename(metadata),
                                                          self.covers_dir)
                
                return {
                    'title': metadata.title,
                    'book_path': book_path,
                    'cover_path': cover_path
                }
        
        # Execute downloads
        tasks = [download_single(metadata) for metadata in metadata_list]
        results_list = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Process results
        for result in results_list:
            if isinstance(result, dict):
                results[result['title']] = result
            elif isinstance(result, Exception):
                logger.error(f"Download failed: {result}")
        
        return results
    
    async def _download_async(self, url: str, filename: str, directory: Path) -> Optional[str]:
        """Asynchronous file download"""
        filepath = directory / filename
        
        if filepath.exists():
            return str(filepath)
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        content = await response.read()
                        
                        # Check size
                        if len(content) > settings.MAX_FILE_SIZE_MB * 1024 * 1024:
                            logger.warning(f"File too large: {filename}")
                            return None
                        
                        with open(filepath, 'wb') as f:
                            f.write(content)
                        
                        return str(filepath)
                    else:
                        logger.error(f"Download failed with status {response.status}: {url}")
                        return None
                        
        except Exception as e:
            logger.error(f"Async download failed: {e}")
            return None
    
    def cleanup_failed_downloads(self):
        """Remove incomplete or corrupted downloads"""
        for directory in [self.books_dir, self.covers_dir]:
            for filepath in directory.iterdir():
                if filepath.is_file():
                    # Check if file is too small (likely incomplete)
                    if filepath.stat().st_size < 1024:
                        logger.info(f"Removing incomplete file: {filepath.name}")
                        filepath.unlink(missing_ok=True)
    
    def get_download_stats(self) -> Dict:
        """Get download statistics"""
        book_count = len(list(self.books_dir.glob('*')))
        cover_count = len(list(self.covers_dir.glob('*')))
        
        book_size = sum(f.stat().st_size for f in self.books_dir.glob('*') if f.is_file())
        cover_size = sum(f.stat().st_size for f in self.covers_dir.glob('*') if f.is_file())
        
        return {
            'books_downloaded': book_count,
            'covers_downloaded': cover_count,
            'total_book_size_mb': book_size / (1024 * 1024),
            'total_cover_size_mb': cover_size / (1024 * 1024),
            'total_files': book_count + cover_count,
        }
    
    def close(self):
        """Close the session"""
        self.session.close()