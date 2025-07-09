"""
Book Metadata Processing Module
Handles metadata extraction, cleaning, and standardization
"""

import json
import csv
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from pathlib import Path

# Simple slugify function to avoid external dependency
def slugify(text: str, max_length: int = 50) -> str:
    """Simple slugify function"""
    if not text:
        return ""
    # Convert to lowercase and replace spaces/special chars with hyphens
    text = re.sub(r'[^\w\s-]', '', text.lower())
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')[:max_length]


class BookMetadata:
    """Standard book metadata structure"""
    
    def __init__(self, title: str = "", author: str = "", isbn: str = "", 
                 year: Optional[int] = None, publisher: str = "", language: str = "",
                 pages: Optional[int] = None, file_format: str = "", file_size: str = "",
                 file_hash: str = "", source: str = "", source_url: str = "",
                 mirrors: List[str] = None, description: str = "", genre: List[str] = None,
                 tags: List[str] = None, cover_url: str = "", download_url: str = "",
                 local_file_path: str = "", local_cover_path: str = "",
                 google_books_data: Dict = None, openlibrary_data: Dict = None,
                 amazon_link: str = "", ebay_link: str = "", google_books_link: str = "",
                 scraped_at: datetime = None, updated_at: datetime = None):
        
                 # Basic Information
         self.title = title
         self.author = author
         self.isbn = isbn
         self.year = year
         self.publisher = publisher
         self.language = language
         self.pages = pages
         
         # File Information
         self.file_format = file_format
         self.file_size = file_size
         self.file_hash = file_hash
         
         # Source Information
         self.source = source
         self.source_url = source_url
         self.mirrors = mirrors or []
         
         # Additional Metadata
         self.description = description
         self.genre = genre or []
         self.tags = tags or []
         self.cover_url = cover_url
         
         # Download Information
         self.download_url = download_url
         self.local_file_path = local_file_path
         self.local_cover_path = local_cover_path
         
         # Enriched Data
         self.google_books_data = google_books_data or {}
         self.openlibrary_data = openlibrary_data or {}
         
         # Affiliate Links
         self.amazon_link = amazon_link
         self.ebay_link = ebay_link
         self.google_books_link = google_books_link
         
         # Timestamps
         self.scraped_at = scraped_at or datetime.now()
         self.updated_at = updated_at or datetime.now()
    
    @property
    def clean_title(self) -> str:
        """Get cleaned title for filename"""
        return slugify(self.title, max_length=50)
    
    @property
    def clean_author(self) -> str:
        """Get cleaned author for filename"""
        return slugify(self.author, max_length=30)
    
        @property
    def filename_base(self) -> str:
        """Get base filename for files"""
        author_part = f"-{self.clean_author}" if self.clean_author else ""
        return f"{self.clean_title}{author_part}"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary for JSON serialization"""
        data = {
            'title': self.title,
            'author': self.author,
            'isbn': self.isbn,
            'year': self.year,
            'publisher': self.publisher,
            'language': self.language,
            'pages': self.pages,
            'file_format': self.file_format,
            'file_size': self.file_size,
            'file_hash': self.file_hash,
            'source': self.source,
            'source_url': self.source_url,
            'mirrors': self.mirrors,
            'description': self.description,
            'genre': self.genre,
            'tags': self.tags,
            'cover_url': self.cover_url,
            'download_url': self.download_url,
            'local_file_path': self.local_file_path,
            'local_cover_path': self.local_cover_path,
            'google_books_data': self.google_books_data,
            'openlibrary_data': self.openlibrary_data,
            'amazon_link': self.amazon_link,
            'ebay_link': self.ebay_link,
            'google_books_link': self.google_books_link,
            'scraped_at': self.scraped_at.isoformat() if self.scraped_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
        return data
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'BookMetadata':
        """Create instance from dictionary"""
        # Convert ISO datetime strings back to datetime objects
        if data.get('scraped_at'):
            data['scraped_at'] = datetime.fromisoformat(data['scraped_at'])
        if data.get('updated_at'):
            data['updated_at'] = datetime.fromisoformat(data['updated_at'])
        return cls(**data)


class MetadataProcessor:
    """Process and enhance book metadata"""
    
    def __init__(self, output_dir: str = "output"):
        self.output_dir = Path(output_dir)
        self.metadata_dir = self.output_dir / "metadata"
        self.metadata_dir.mkdir(parents=True, exist_ok=True)
    
    def clean_text(self, text: str) -> str:
        """Clean and normalize text"""
        if not text:
            return ""
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove HTML tags
        text = re.sub(r'<[^>]+>', '', text)
        
        # Remove special characters but keep basic punctuation
        text = re.sub(r'[^\w\s\-.,;:!?()[\]{}]', '', text)
        
        return text
    
    def extract_isbn(self, text: str) -> str:
        """Extract ISBN from text"""
        # Look for ISBN-13 (978/979 prefix)
        isbn13_pattern = r'(?:ISBN[-\s]?(?:13)?[-\s]?:?\s?)?(?:978|979)[-\s]?\d[-\s]?\d{2}[-\s]?\d{6}[-\s]?\d'
        match = re.search(isbn13_pattern, text.replace('-', '').replace(' ', ''))
        if match:
            return re.sub(r'[^\d]', '', match.group())
        
        # Look for ISBN-10
        isbn10_pattern = r'(?:ISBN[-\s]?(?:10)?[-\s]?:?\s?)?\d{9}[\dXx]'
        match = re.search(isbn10_pattern, text.replace('-', '').replace(' ', ''))
        if match:
            return re.sub(r'[^\dXx]', '', match.group()).upper()
        
        return ""
    
    def extract_year(self, text: str) -> Optional[int]:
        """Extract publication year from text"""
        # Look for 4-digit year between 1500-2030
        year_pattern = r'\b(1[5-9]\d{2}|20[0-3]\d)\b'
        matches = re.findall(year_pattern, text)
        if matches:
            # Return the most recent year found
            return max(int(year) for year in matches)
        return None
    
    def extract_file_size(self, text: str) -> str:
        """Extract file size from text"""
        size_pattern = r'(\d+(?:\.\d+)?)\s*(B|KB|MB|GB|TB)'
        match = re.search(size_pattern, text, re.IGNORECASE)
        if match:
            return f"{match.group(1)} {match.group(2).upper()}"
        return ""
    
    def process_metadata(self, raw_data: Dict, source: str = "") -> BookMetadata:
        """Process raw scraped data into standardized metadata"""
        
        # Extract and clean basic info
        title = self.clean_text(raw_data.get('title', ''))
        author = self.clean_text(raw_data.get('author', ''))
        
        # Extract structured data
        isbn = self.extract_isbn(raw_data.get('isbn', '') or raw_data.get('identifier', ''))
        year = self.extract_year(raw_data.get('year', '') or raw_data.get('date', '') or title)
        
        # Create metadata object
        metadata = BookMetadata(
            title=title,
            author=author,
            isbn=isbn,
            year=year,
            publisher=self.clean_text(raw_data.get('publisher', '')),
            language=raw_data.get('language', ''),
            pages=self._safe_int(raw_data.get('pages')),
            file_format=raw_data.get('format', '').upper(),
            file_size=self.extract_file_size(raw_data.get('filesize', '')),
            source=source,
            source_url=raw_data.get('url', ''),
            description=self.clean_text(raw_data.get('description', '')),
            cover_url=raw_data.get('cover_url', ''),
            download_url=raw_data.get('download_url', ''),
            mirrors=raw_data.get('mirrors', [])
        )
        
        return metadata
    
    def _safe_int(self, value: Any) -> Optional[int]:
        """Safely convert value to integer"""
        if value is None:
            return None
        try:
            if isinstance(value, str):
                # Extract first number from string
                match = re.search(r'\d+', value)
                return int(match.group()) if match else None
            return int(value)
        except (ValueError, TypeError):
            return None
    
    def save_metadata_json(self, metadata: BookMetadata) -> str:
        """Save metadata as JSON file"""
        filename = f"{metadata.filename_base}.json"
        filepath = self.metadata_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(metadata.to_dict(), f, indent=2, ensure_ascii=False)
        
        return str(filepath)
    
    def save_metadata_csv(self, metadata_list: List[BookMetadata], filename: str = "books.csv") -> str:
        """Save multiple metadata entries as CSV"""
        filepath = self.metadata_dir / filename
        
        if not metadata_list:
            return str(filepath)
        
        fieldnames = metadata_list[0].to_dict().keys()
        
        with open(filepath, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for metadata in metadata_list:
                writer.writerow(metadata.to_dict())
        
        return str(filepath)
    
    def load_metadata_json(self, filepath: str) -> BookMetadata:
        """Load metadata from JSON file"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return BookMetadata.from_dict(data)
    
    def validate_metadata(self, metadata: BookMetadata) -> List[str]:
        """Validate metadata and return list of issues"""
        issues = []
        
        if not metadata.title:
            issues.append("Missing title")
        
        if not metadata.author:
            issues.append("Missing author")
        
        if not metadata.download_url and not metadata.local_file_path:
            issues.append("No download URL or local file path")
        
        if metadata.isbn and not self._is_valid_isbn(metadata.isbn):
            issues.append("Invalid ISBN format")
        
        return issues
    
    def _is_valid_isbn(self, isbn: str) -> bool:
        """Validate ISBN format"""
        isbn = re.sub(r'[^\dXx]', '', isbn).upper()
        
        if len(isbn) == 10:
            # ISBN-10 validation
            return True  # Simplified validation
        elif len(isbn) == 13:
            # ISBN-13 validation
            return isbn.startswith(('978', '979'))
        
        return False