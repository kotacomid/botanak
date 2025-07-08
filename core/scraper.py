"""
Main Book Scraping Module
Handles scraping from Anna's Archive and LibGen
"""

import time
import requests
import asyncio
import aiohttp
from bs4 import BeautifulSoup
from typing import Dict, List, Optional, Any
from urllib.parse import urljoin, quote
import logging
from abc import ABC, abstractmethod

from config.settings import settings
from .metadata import MetadataProcessor, BookMetadata


# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Base class for all book scrapers"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': settings.USER_AGENT,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
        self.metadata_processor = MetadataProcessor()
    
    @abstractmethod
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Search for books with given query"""
        pass
    
    @abstractmethod
    def get_book_details(self, book_url: str) -> Dict:
        """Get detailed information for a specific book"""
        pass
    
    def _make_request(self, url: str, retries: int = None) -> requests.Response:
        """Make HTTP request with retry logic"""
        retries = retries or settings.MAX_RETRIES
        
        for attempt in range(retries):
            try:
                response = self.session.get(url, timeout=settings.TIMEOUT)
                response.raise_for_status()
                
                # Respect rate limiting
                time.sleep(settings.SCRAPING_DELAY)
                
                return response
                
            except requests.RequestException as e:
                logger.warning(f"Request failed (attempt {attempt + 1}/{retries}): {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
                else:
                    raise
    
    def close(self):
        """Close the session"""
        self.session.close()


class AnnasArchiveScraper(BaseScraper):
    """Scraper for Anna's Archive"""
    
    def __init__(self):
        super().__init__()
        self.base_url = settings.ANNAS_ARCHIVE_URL
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Search Anna's Archive for books"""
        search_url = f"{self.base_url}/search"
        params = {
            'q': query,
            'sort': 'newest',
            'ext': 'pdf'  # Focus on PDF files
        }
        
        try:
            response = self._make_request(search_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            results = []
            book_items = soup.find_all('div', class_='js-scroll-hidden')[:limit]
            
            for item in book_items:
                book_data = self._parse_search_result(item)
                if book_data:
                    results.append(book_data)
            
            logger.info(f"Found {len(results)} books on Anna's Archive for query: {query}")
            return results
            
        except Exception as e:
            logger.error(f"Error searching Anna's Archive: {e}")
            return []
    
    def _parse_search_result(self, item) -> Optional[Dict]:
        """Parse individual search result"""
        try:
            # Extract title and author
            title_elem = item.find('h3')
            title = title_elem.get_text(strip=True) if title_elem else ""
            
            # Extract metadata
            metadata_elem = item.find('div', class_='text-sm')
            metadata_text = metadata_elem.get_text() if metadata_elem else ""
            
            # Extract download link
            link_elem = item.find('a', href=True)
            book_url = urljoin(self.base_url, link_elem['href']) if link_elem else ""
            
            return {
                'title': title,
                'metadata_raw': metadata_text,
                'url': book_url,
                'source': 'annas-archive'
            }
            
        except Exception as e:
            logger.warning(f"Error parsing search result: {e}")
            return None
    
    def get_book_details(self, book_url: str) -> Dict:
        """Get detailed book information from Anna's Archive"""
        try:
            response = self._make_request(book_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract detailed metadata
            details = {
                'url': book_url,
                'source': 'annas-archive'
            }
            
            # Title
            title_elem = soup.find('h1')
            if title_elem:
                details['title'] = title_elem.get_text(strip=True)
            
            # Metadata table
            metadata_rows = soup.find_all('tr')
            for row in metadata_rows:
                cells = row.find_all(['td', 'th'])
                if len(cells) >= 2:
                    key = cells[0].get_text(strip=True).lower()
                    value = cells[1].get_text(strip=True)
                    
                    if 'author' in key:
                        details['author'] = value
                    elif 'publisher' in key:
                        details['publisher'] = value
                    elif 'year' in key or 'date' in key:
                        details['year'] = value
                    elif 'isbn' in key:
                        details['isbn'] = value
                    elif 'language' in key:
                        details['language'] = value
                    elif 'pages' in key:
                        details['pages'] = value
                    elif 'filesize' in key or 'size' in key:
                        details['filesize'] = value
                    elif 'format' in key:
                        details['format'] = value
            
            # Download links
            download_links = soup.find_all('a', href=True)
            mirrors = []
            download_url = ""
            
            for link in download_links:
                href = link.get('href', '')
                if any(mirror in href for mirror in ['libgen', 'download', 'mirror']):
                    full_url = urljoin(self.base_url, href)
                    mirrors.append(full_url)
                    if not download_url:
                        download_url = full_url
            
            details['download_url'] = download_url
            details['mirrors'] = mirrors
            
            # Cover image
            img_elem = soup.find('img', src=True)
            if img_elem and 'cover' in img_elem.get('src', '').lower():
                details['cover_url'] = urljoin(self.base_url, img_elem['src'])
            
            return details
            
        except Exception as e:
            logger.error(f"Error getting book details from Anna's Archive: {e}")
            return {'url': book_url, 'source': 'annas-archive'}


class LibGenScraper(BaseScraper):
    """Scraper for LibGen"""
    
    def __init__(self):
        super().__init__()
        self.base_urls = settings.LIBGEN_URLS
        self.current_url = self.base_urls[0]
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Search LibGen for books"""
        search_url = f"{self.current_url}/search.php"
        params = {
            'req': query,
            'column': 'def',
            'sort': 'year',
            'sortmode': 'DESC'
        }
        
        try:
            response = self._make_request(search_url, params=params)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            results = []
            
            # Find the results table
            table = soup.find('table', class_='c')
            if not table:
                return results
            
            rows = table.find_all('tr')[1:limit+1]  # Skip header row
            
            for row in rows:
                book_data = self._parse_libgen_row(row)
                if book_data:
                    results.append(book_data)
            
            logger.info(f"Found {len(results)} books on LibGen for query: {query}")
            return results
            
        except Exception as e:
            logger.error(f"Error searching LibGen: {e}")
            return []
    
    def _parse_libgen_row(self, row) -> Optional[Dict]:
        """Parse LibGen table row"""
        try:
            cells = row.find_all('td')
            if len(cells) < 10:
                return None
            
            # Extract data from cells
            details = {
                'source': 'libgen',
                'title': cells[2].get_text(strip=True),
                'author': cells[1].get_text(strip=True),
                'year': cells[4].get_text(strip=True),
                'pages': cells[5].get_text(strip=True),
                'language': cells[6].get_text(strip=True),
                'filesize': cells[7].get_text(strip=True),
                'format': cells[8].get_text(strip=True),
            }
            
            # Get download link
            download_cell = cells[9] if len(cells) > 9 else cells[-1]
            link_elem = download_cell.find('a', href=True)
            if link_elem:
                details['download_url'] = urljoin(self.current_url, link_elem['href'])
            
            return details
            
        except Exception as e:
            logger.warning(f"Error parsing LibGen row: {e}")
            return None
    
    def get_book_details(self, book_url: str) -> Dict:
        """Get detailed book information from LibGen"""
        try:
            response = self._make_request(book_url)
            soup = BeautifulSoup(response.content, 'html.parser')
            
            details = {
                'url': book_url,
                'source': 'libgen'
            }
            
            # Extract additional details from the book page
            # LibGen book pages have detailed information
            
            return details
            
        except Exception as e:
            logger.error(f"Error getting book details from LibGen: {e}")
            return {'url': book_url, 'source': 'libgen'}


class BookScraper:
    """Main scraper that coordinates multiple sources"""
    
    def __init__(self):
        self.scrapers = {
            'annas-archive': AnnasArchiveScraper(),
            'libgen': LibGenScraper()
        }
        self.metadata_processor = MetadataProcessor()
    
    def search_all_sources(self, query: str, limit_per_source: int = 5) -> List[BookMetadata]:
        """Search all sources and return unified results"""
        all_results = []
        
        for source_name, scraper in self.scrapers.items():
            try:
                logger.info(f"Searching {source_name} for: {query}")
                results = scraper.search(query, limit_per_source)
                
                for result in results:
                    # Get detailed information
                    if result.get('url'):
                        detailed = scraper.get_book_details(result['url'])
                        result.update(detailed)
                    
                    # Process into standardized metadata
                    metadata = self.metadata_processor.process_metadata(result, source_name)
                    all_results.append(metadata)
                    
            except Exception as e:
                logger.error(f"Error searching {source_name}: {e}")
                continue
        
        logger.info(f"Total results found: {len(all_results)}")
        return all_results
    
    def search_book(self, title: str, author: str = "", source: str = None) -> List[BookMetadata]:
        """Search for a specific book"""
        query = f"{title} {author}".strip()
        
        if source and source in self.scrapers:
            scraper = self.scrapers[source]
            results = scraper.search(query, 10)
            processed_results = []
            
            for result in results:
                if result.get('url'):
                    detailed = scraper.get_book_details(result['url'])
                    result.update(detailed)
                
                metadata = self.metadata_processor.process_metadata(result, source)
                processed_results.append(metadata)
            
            return processed_results
        else:
            return self.search_all_sources(query, 5)
    
    def close(self):
        """Close all scrapers"""
        for scraper in self.scrapers.values():
            scraper.close()