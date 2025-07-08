"""
Affiliate Link Generator
Creates affiliate links for monetization
"""

import requests
import urllib.parse
from typing import Optional, Dict
import logging

from config.settings import settings
from core.metadata import BookMetadata

logger = logging.getLogger(__name__)


class AffiliateLinker:
    """Generate affiliate links for books"""
    
    def __init__(self):
        self.amazon_tag = settings.AMAZON_AFFILIATE_TAG
        self.ebay_id = settings.EBAY_AFFILIATE_ID
    
    def enrich_metadata(self, metadata: BookMetadata) -> BookMetadata:
        """Add affiliate links to book metadata"""
        
        # Generate Amazon link
        if self.amazon_tag and metadata.isbn:
            metadata.amazon_link = self.generate_amazon_link(
                metadata.title, metadata.author, metadata.isbn
            )
        
        # Generate eBay link
        if self.ebay_id:
            metadata.ebay_link = self.generate_ebay_link(
                metadata.title, metadata.author
            )
        
        # Generate Google Books link
        if metadata.isbn:
            metadata.google_books_link = self.generate_google_books_link(metadata.isbn)
        
        return metadata
    
    def generate_amazon_link(self, title: str, author: str = "", isbn: str = "") -> str:
        """Generate Amazon affiliate link"""
        if not self.amazon_tag:
            return ""
        
        try:
            # Use ISBN if available for more accurate results
            if isbn:
                search_term = isbn
            else:
                search_term = f"{title} {author}".strip()
            
            # Amazon search URL with affiliate tag
            base_url = "https://www.amazon.com/s"
            params = {
                'k': search_term,
                'ref': 'sr_st_relevancerank',
                'tag': self.amazon_tag
            }
            
            return f"{base_url}?{urllib.parse.urlencode(params)}"
            
        except Exception as e:
            logger.error(f"Error generating Amazon link: {e}")
            return ""
    
    def generate_ebay_link(self, title: str, author: str = "") -> str:
        """Generate eBay affiliate link"""
        if not self.ebay_id:
            return ""
        
        try:
            search_term = f"{title} {author}".strip()
            
            # eBay Partner Network URL
            base_url = "https://www.ebay.com/sch/i.html"
            params = {
                '_nkw': search_term,
                '_sacat': '267',  # Books category
                'mkcid': '1',
                'mkrid': '711-53200-19255-0',
                'siteid': '0',
                'campid': self.ebay_id,
                'customid': '',
                'toolid': '10001'
            }
            
            return f"{base_url}?{urllib.parse.urlencode(params)}"
            
        except Exception as e:
            logger.error(f"Error generating eBay link: {e}")
            return ""
    
    def generate_google_books_link(self, isbn: str) -> str:
        """Generate Google Books link"""
        if not isbn:
            return ""
        
        try:
            return f"https://books.google.com/books?isbn={isbn}"
        except Exception as e:
            logger.error(f"Error generating Google Books link: {e}")
            return ""
    
    def generate_bookdepository_link(self, isbn: str) -> str:
        """Generate Book Depository affiliate link"""
        if not isbn:
            return ""
        
        try:
            return f"https://www.bookdepository.com/search?searchTerm={isbn}"
        except Exception as e:
            logger.error(f"Error generating Book Depository link: {e}")
            return ""
    
    def generate_thriftbooks_link(self, title: str, author: str = "") -> str:
        """Generate ThriftBooks link"""
        try:
            search_term = f"{title} {author}".strip()
            encoded_term = urllib.parse.quote_plus(search_term)
            return f"https://www.thriftbooks.com/browse/?b.search={encoded_term}"
        except Exception as e:
            logger.error(f"Error generating ThriftBooks link: {e}")
            return ""
    
    def get_price_comparison_links(self, metadata: BookMetadata) -> Dict[str, str]:
        """Get price comparison links from multiple sources"""
        links = {}
        
        if metadata.amazon_link:
            links['Amazon'] = metadata.amazon_link
        
        if metadata.ebay_link:
            links['eBay'] = metadata.ebay_link
        
        if metadata.google_books_link:
            links['Google Books'] = metadata.google_books_link
        
        # Add more comparison sites
        if metadata.isbn:
            links['Book Depository'] = self.generate_bookdepository_link(metadata.isbn)
        
        links['ThriftBooks'] = self.generate_thriftbooks_link(
            metadata.title, metadata.author
        )
        
        return {k: v for k, v in links.items() if v}  # Remove empty links
    
    def track_click(self, book_id: str, affiliate_source: str) -> bool:
        """Track affiliate link clicks for analytics"""
        try:
            # This could be implemented with your analytics system
            logger.info(f"Affiliate click tracked: {book_id} -> {affiliate_source}")
            return True
        except Exception as e:
            logger.error(f"Error tracking affiliate click: {e}")
            return False