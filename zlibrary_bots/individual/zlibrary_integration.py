#!/usr/bin/env python3
"""
Z-Library Integration for Book Scraping Bot
Shows how to add Z-Library as a source to your existing bot
"""

import asyncio
import json
from pathlib import Path
from typing import List, Dict, Optional
from dataclasses import dataclass

# Check for zlibrary availability
try:
    import zlibrary
    from zlibrary import Language, Extension
    ZLIBRARY_AVAILABLE = True
except ImportError:
    ZLIBRARY_AVAILABLE = False
    print("⚠️ zlibrary package not available - Z-Library features disabled")


@dataclass
class UnifiedBookResult:
    """Unified book result structure for all sources"""
    title: str
    authors: List[str]
    year: Optional[str] = None
    isbn: Optional[str] = None
    publisher: Optional[str] = None
    language: Optional[str] = None
    file_format: Optional[str] = None
    file_size: Optional[str] = None
    rating: Optional[str] = None
    download_url: Optional[str] = None
    cover_url: Optional[str] = None
    source: str = "unknown"
    
    def to_dict(self) -> Dict:
        """Convert to dictionary"""
        result = {}
        for key, value in self.__dict__.items():
            if value is not None:
                result[key] = value
        return result


class ZLibrarySource:
    """Z-Library source for the book scraping bot"""
    
    def __init__(self, email: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize Z-Library source
        
        Args:
            email: Z-Library account email (optional)
            password: Z-Library account password (optional)
        """
        self.email = email
        self.password = password
        self.lib = None
        self.authenticated = False
        self.enabled = ZLIBRARY_AVAILABLE
        
    async def connect(self) -> bool:
        """Connect to Z-Library"""
        if not self.enabled:
            return False
            
        try:
            self.lib = zlibrary.AsyncZlib()
            
            if self.email and self.password:
                await self.lib.login(self.email, self.password)
                self.authenticated = True
                print("✅ Z-Library authenticated")
            
            return True
            
        except Exception as e:
            print(f"❌ Z-Library connection failed: {e}")
            return False
    
    async def search(self, query: str, count: int = 10, **filters) -> List[UnifiedBookResult]:
        """
        Search Z-Library for books
        
        Args:
            query: Search query
            count: Number of results
            **filters: Additional filters (year_from, year_to, language, format)
            
        Returns:
            List of unified book results
        """
        if not self.enabled or not self.lib:
            return []
        
        try:
            # Build search parameters
            search_params = {'q': query, 'count': count}
            
            # Apply filters
            if 'year_from' in filters:
                search_params['from_year'] = filters['year_from']
            if 'year_to' in filters:
                search_params['to_year'] = filters['year_to']
            
            # Convert language filter
            if 'language' in filters:
                lang_map = {
                    'english': Language.ENGLISH,
                    'russian': Language.RUSSIAN,
                    'german': Language.GERMAN,
                    'french': Language.FRENCH,
                    'spanish': Language.SPANISH
                }
                if filters['language'].lower() in lang_map:
                    search_params['lang'] = [lang_map[filters['language'].lower()]]
            
            # Convert format filter
            if 'format' in filters:
                format_map = {
                    'pdf': Extension.PDF,
                    'epub': Extension.EPUB,
                    'mobi': Extension.MOBI,
                    'txt': Extension.TXT,
                    'doc': Extension.DOC
                }
                if filters['format'].lower() in format_map:
                    search_params['extensions'] = [format_map[filters['format'].lower()]]
            
            # Perform search
            paginator = await self.lib.search(**search_params)
            results = await paginator.next()
            
            # Convert to unified format
            unified_results = []
            for book in results:
                authors = [author.get('author', '') for author in book.get('authors', [])]
                
                unified_book = UnifiedBookResult(
                    title=book.get('name', ''),
                    authors=authors,
                    year=book.get('year'),
                    isbn=book.get('isbn'),
                    publisher=book.get('publisher'),
                    language=book.get('language'),
                    file_format=book.get('extension'),
                    file_size=book.get('size'),
                    rating=book.get('rating'),
                    download_url=book.get('url'),
                    cover_url=book.get('cover'),
                    source="Z-Library"
                )
                unified_results.append(unified_book)
            
            return unified_results
            
        except Exception as e:
            print(f"❌ Z-Library search failed: {e}")
            return []
    
    async def get_limits(self) -> Dict:
        """Get download limits"""
        if not self.enabled or not self.lib or not self.authenticated:
            return {}
        
        try:
            return await self.lib.profile.get_limits()
        except Exception as e:
            print(f"❌ Failed to get Z-Library limits: {e}")
            return {}


class EnhancedBookScrapingBot:
    """Enhanced book scraping bot with Z-Library integration"""
    
    def __init__(self, zlibrary_email: Optional[str] = None, zlibrary_password: Optional[str] = None):
        """
        Initialize enhanced bot
        
        Args:
            zlibrary_email: Z-Library email (optional)
            zlibrary_password: Z-Library password (optional)
        """
        # Initialize sources
        self.zlibrary = ZLibrarySource(zlibrary_email, zlibrary_password)
        
        # Statistics
        self.stats = {
            'total_searches': 0,
            'zlibrary_results': 0,
            'annas_archive_results': 0,
            'libgen_results': 0
        }
    
    async def connect_sources(self):
        """Connect to all available sources"""
        print("🔗 Connecting to book sources...")
        
        # Connect Z-Library
        if await self.zlibrary.connect():
            print("  ✅ Z-Library connected")
        else:
            print("  ❌ Z-Library unavailable")
        
        # Here you would connect other sources (Anna's Archive, LibGen)
        print("  ✅ Other sources ready")
    
    async def search_all_sources(self, query: str, count_per_source: int = 10, **filters) -> Dict[str, List[UnifiedBookResult]]:
        """
        Search all available sources
        
        Args:
            query: Search query
            count_per_source: Results per source
            **filters: Search filters
            
        Returns:
            Dictionary of results by source
        """
        self.stats['total_searches'] += 1
        results = {}
        
        print(f"🔍 Searching all sources for: '{query}'")
        
        # Search Z-Library
        if self.zlibrary.enabled:
            zlibrary_results = await self.zlibrary.search(query, count_per_source, **filters)
            results['Z-Library'] = zlibrary_results
            self.stats['zlibrary_results'] += len(zlibrary_results)
            print(f"  📚 Z-Library: {len(zlibrary_results)} results")
        
        # Here you would search other sources
        # Anna's Archive simulation
        results['Anna\'s Archive'] = []  # Your existing Anna's Archive search
        results['LibGen'] = []  # Your existing LibGen search
        
        return results
    
    async def search_with_fallback(self, query: str, preferred_source: str = "Z-Library", **filters) -> List[UnifiedBookResult]:
        """
        Search with fallback to other sources
        
        Args:
            query: Search query
            preferred_source: Preferred source to try first
            **filters: Search filters
            
        Returns:
            Combined results from available sources
        """
        all_results = []
        
        # Try preferred source first
        if preferred_source == "Z-Library" and self.zlibrary.enabled:
            results = await self.zlibrary.search(query, 10, **filters)
            all_results.extend(results)
            
            if results:
                print(f"✅ Found {len(results)} results from Z-Library")
                return all_results
        
        # Fallback to other sources if preferred source has no results
        print("🔄 Trying other sources...")
        
        # Here you would implement fallback to Anna's Archive, LibGen
        # For demo, we'll just return Z-Library results
        if not all_results and self.zlibrary.enabled:
            results = await self.zlibrary.search(query, 20, **filters)
            all_results.extend(results)
        
        return all_results
    
    def save_results(self, results: List[UnifiedBookResult], filename: str = None):
        """Save unified results to file"""
        if not results:
            return
        
        # Create output directory
        output_dir = Path("enhanced_bot_output")
        output_dir.mkdir(exist_ok=True)
        
        # Generate filename if not provided
        if not filename:
            timestamp = asyncio.get_event_loop().time()
            filename = f"search_results_{int(timestamp)}.json"
        
        output_file = output_dir / filename
        
        # Convert to serializable format
        serializable_results = [book.to_dict() for book in results]
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(serializable_results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {output_file}")
    
    def display_results(self, results: List[UnifiedBookResult], max_display: int = 10):
        """Display results in a formatted way"""
        if not results:
            print("No results to display")
            return
        
        print(f"\n📚 Displaying {min(len(results), max_display)} of {len(results)} results:")
        print("=" * 80)
        
        for i, book in enumerate(results[:max_display], 1):
            authors_str = ", ".join(book.authors) if book.authors else "Unknown"
            
            print(f"\n{i}. {book.title}")
            print(f"   👤 Authors: {authors_str}")
            print(f"   📅 Year: {book.year or 'Unknown'}")
            print(f"   📄 Format: {book.file_format or 'Unknown'}")
            print(f"   📏 Size: {book.file_size or 'Unknown'}")
            print(f"   ⭐ Rating: {book.rating or 'No rating'}")
            print(f"   🌐 Source: {book.source}")
            
            if book.publisher:
                print(f"   🏢 Publisher: {book.publisher}")
    
    def get_stats(self) -> Dict:
        """Get bot statistics"""
        return self.stats.copy()
    
    async def get_source_status(self) -> Dict:
        """Get status of all sources"""
        status = {
            'Z-Library': {
                'available': self.zlibrary.enabled,
                'authenticated': self.zlibrary.authenticated,
                'limits': await self.zlibrary.get_limits() if self.zlibrary.authenticated else {}
            },
            'Anna\'s Archive': {'available': True, 'authenticated': False},  # Your implementation
            'LibGen': {'available': True, 'authenticated': False}  # Your implementation
        }
        return status


# Example usage functions
async def example_basic_integration():
    """Example: Basic integration usage"""
    print("🔹 EXAMPLE: Basic Integration")
    print("-" * 35)
    
    # Initialize enhanced bot
    bot = EnhancedBookScrapingBot()
    await bot.connect_sources()
    
    # Search all sources
    all_results = await bot.search_all_sources("python programming", count_per_source=5)
    
    # Display results by source
    for source, results in all_results.items():
        if results:
            print(f"\n📚 {source} Results:")
            bot.display_results(results, max_display=3)
    
    # Save combined results
    combined_results = []
    for results in all_results.values():
        combined_results.extend(results)
    
    bot.save_results(combined_results, "combined_search.json")


async def example_filtered_search():
    """Example: Search with filters"""
    print("\n🔹 EXAMPLE: Filtered Search")
    print("-" * 30)
    
    bot = EnhancedBookScrapingBot()
    await bot.connect_sources()
    
    # Search with filters
    results = await bot.search_with_fallback(
        "machine learning",
        preferred_source="Z-Library",
        year_from=2020,
        language="english",
        format="pdf"
    )
    
    bot.display_results(results)
    print(f"\n📊 Statistics: {bot.get_stats()}")


async def example_with_authentication():
    """Example: Using with Z-Library authentication"""
    print("\n🔹 EXAMPLE: With Authentication")
    print("-" * 40)
    
    # Initialize with credentials (replace with actual credentials)
    email = None  # "your_email@example.com"
    password = None  # "your_password"
    
    bot = EnhancedBookScrapingBot(email, password)
    await bot.connect_sources()
    
    # Check source status
    status = await bot.get_source_status()
    print("📊 Source Status:")
    for source, info in status.items():
        auth_status = "✅ Authenticated" if info['authenticated'] else "❌ Not authenticated"
        avail_status = "✅ Available" if info['available'] else "❌ Unavailable"
        print(f"  {source}: {avail_status}, {auth_status}")
        
        if info['limits']:
            print(f"    📥 Limits: {info['limits']}")


async def main():
    """Main demonstration"""
    print("🚀 Enhanced Book Scraping Bot with Z-Library Integration")
    print("=" * 60)
    
    try:
        await example_basic_integration()
        await example_filtered_search()
        await example_with_authentication()
        
        print("\n✅ Integration examples completed!")
        print("📁 Check 'enhanced_bot_output' folder for results")
        
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())