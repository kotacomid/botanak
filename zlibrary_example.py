#!/usr/bin/env python3
"""
Simple Z-Library Example Script
Demonstrates key functionality of the zlibrary package in an easy-to-use format
"""

import asyncio
import json
from pathlib import Path
from typing import List, Dict, Optional
try:
    import zlibrary
    from zlibrary import Language, Extension
except ImportError:
    print("❌ zlibrary package not installed. Run: pip install zlibrary")
    exit(1)


class SimpleZLibrary:
    """Simple Z-Library interface with essential functionality"""
    
    def __init__(self, email: Optional[str] = None, password: Optional[str] = None):
        """
        Initialize with optional credentials
        
        Args:
            email: Z-Library account email (optional)
            password: Z-Library account password (optional)
        """
        self.email = email
        self.password = password
        self.lib = None
        self.authenticated = False
        
    async def __aenter__(self):
        """Async context manager entry"""
        await self.connect()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        pass
        
    async def connect(self):
        """Connect to Z-Library"""
        self.lib = zlibrary.AsyncZlib()
        
        if self.email and self.password:
            try:
                await self.lib.login(self.email, self.password)
                self.authenticated = True
                print("✅ Successfully logged in to Z-Library")
            except Exception as e:
                print(f"⚠️ Login failed: {e}")
        else:
            print("ℹ️ Running without authentication (limited features)")
            
    async def search(self, query: str, count: int = 10) -> List[Dict]:
        """
        Search for books
        
        Args:
            query: Search term
            count: Number of results
            
        Returns:
            List of book dictionaries
        """
        if not self.lib:
            raise RuntimeError("Not connected. Use 'async with SimpleZLibrary()' context manager.")
            
        print(f"🔍 Searching for: {query}")
        
        try:
            paginator = await self.lib.search(q=query, count=count)
            results = await paginator.next()
            
            print(f"✅ Found {len(results)} books")
            return results
            
        except Exception as e:
            print(f"❌ Search failed: {e}")
            return []
    
    async def search_advanced(self, 
                            query: str, 
                            count: int = 10,
                            from_year: Optional[int] = None,
                            to_year: Optional[int] = None,
                            language: Optional[str] = None,
                            file_format: Optional[str] = None) -> List[Dict]:
        """
        Advanced search with filters
        
        Args:
            query: Search term
            count: Number of results
            from_year: Start year (e.g., 2020)
            to_year: End year (e.g., 2023)
            language: Language code ('english', 'russian', etc.)
            file_format: File format ('pdf', 'epub', etc.)
            
        Returns:
            List of book dictionaries
        """
        if not self.lib:
            raise RuntimeError("Not connected. Use 'async with SimpleZLibrary()' context manager.")
            
        print(f"🔍 Advanced search for: {query}")
        
        # Build search parameters
        search_params = {'q': query, 'count': count}
        
        if from_year:
            search_params['from_year'] = from_year
        if to_year:
            search_params['to_year'] = to_year
        if language:
            # Convert string to Language enum
            lang_mapping = {
                'english': Language.ENGLISH,
                'russian': Language.RUSSIAN,
                'german': Language.GERMAN,
                'french': Language.FRENCH,
                'spanish': Language.SPANISH,
                'italian': Language.ITALIAN,
                'chinese': Language.CHINESE,
                'japanese': Language.JAPANESE
            }
            if language.lower() in lang_mapping:
                search_params['lang'] = [lang_mapping[language.lower()]]
        
        if file_format:
            # Convert string to Extension enum
            ext_mapping = {
                'pdf': Extension.PDF,
                'epub': Extension.EPUB,
                'mobi': Extension.MOBI,
                'azw': Extension.AZW,
                'azw3': Extension.AZW3,
                'fb2': Extension.FB2,
                'txt': Extension.TXT,
                'rtf': Extension.RTF,
                'doc': Extension.DOC,
                'docx': Extension.DOCX
            }
            if file_format.lower() in ext_mapping:
                search_params['extensions'] = [ext_mapping[file_format.lower()]]
        
        try:
            paginator = await self.lib.search(**search_params)
            results = await paginator.next()
            
            print(f"✅ Found {len(results)} books with filters")
            return results
            
        except Exception as e:
            print(f"❌ Advanced search failed: {e}")
            return []
    
    async def full_text_search(self, query: str, exact_phrase: bool = False) -> List[Dict]:
        """
        Search inside book contents
        
        Args:
            query: Text to search for inside books
            exact_phrase: Whether to search for exact phrase
            
        Returns:
            List of book dictionaries
        """
        if not self.lib:
            raise RuntimeError("Not connected. Use 'async with SimpleZLibrary()' context manager.")
            
        print(f"📖 Full-text search for: '{query}'")
        
        try:
            paginator = await self.lib.full_text_search(
                q=query, 
                phrase=exact_phrase, 
                exact=exact_phrase
            )
            results = await paginator.next()
            
            print(f"✅ Found {len(results)} books containing the text")
            return results
            
        except Exception as e:
            print(f"❌ Full-text search failed: {e}")
            return []
    
    async def get_limits(self) -> Dict:
        """Get download limits (requires authentication)"""
        if not self.lib or not self.authenticated:
            print("⚠️ Authentication required for download limits")
            return {}
            
        try:
            limits = await self.lib.profile.get_limits()
            return limits
        except Exception as e:
            print(f"❌ Failed to get limits: {e}")
            return {}
    
    def save_results(self, results: List[Dict], filename: str = "zlibrary_results.json"):
        """
        Save search results to JSON file
        
        Args:
            results: List of book dictionaries
            filename: Output filename
        """
        if not results:
            print("No results to save")
            return
            
        # Create output directory
        Path("zlibrary_output").mkdir(exist_ok=True)
        output_path = Path("zlibrary_output") / filename
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
            
        print(f"💾 Results saved to: {output_path}")
    
    def print_results(self, results: List[Dict], max_results: int = 10):
        """
        Print search results in a nice format
        
        Args:
            results: List of book dictionaries
            max_results: Maximum number of results to display
        """
        if not results:
            print("No results to display")
            return
            
        print(f"\n📚 Showing {min(len(results), max_results)} of {len(results)} results:")
        print("=" * 80)
        
        for i, book in enumerate(results[:max_results]):
            authors = book.get('authors', [])
            author_names = ", ".join([author.get('author', '') for author in authors])
            
            print(f"\n{i+1}. {book.get('name', 'Unknown Title')}")
            print(f"   📝 Author(s): {author_names}")
            print(f"   📅 Year: {book.get('year', 'Unknown')}")
            print(f"   📄 Format: {book.get('extension', 'Unknown')}")
            print(f"   📏 Size: {book.get('size', 'Unknown')}")
            print(f"   ⭐ Rating: {book.get('rating', 'No rating')}")
            print(f"   🏢 Publisher: {book.get('publisher', 'Unknown')}")
            print(f"   🌐 URL: {book.get('url', 'N/A')}")


# Example usage functions
async def example_basic_search():
    """Example: Basic book search"""
    print("\n🔹 EXAMPLE 1: Basic Search")
    print("-" * 40)
    
    async with SimpleZLibrary() as zlib:
        # Search for programming books
        results = await zlib.search("python programming", count=5)
        zlib.print_results(results)
        zlib.save_results(results, "python_books.json")


async def example_advanced_search():
    """Example: Advanced search with filters"""
    print("\n🔹 EXAMPLE 2: Advanced Search with Filters")
    print("-" * 50)
    
    async with SimpleZLibrary() as zlib:
        # Search for recent Python books in PDF format
        results = await zlib.search_advanced(
            query="machine learning",
            count=5,
            from_year=2020,
            to_year=2024,
            language="english",
            file_format="pdf"
        )
        zlib.print_results(results)


async def example_full_text_search():
    """Example: Full-text search"""
    print("\n🔹 EXAMPLE 3: Full-Text Search")
    print("-" * 35)
    
    async with SimpleZLibrary() as zlib:
        # Search for books containing specific text
        results = await zlib.full_text_search(
            "neural networks and deep learning",
            exact_phrase=True
        )
        zlib.print_results(results, max_results=3)


async def example_with_authentication():
    """Example: Using with authentication (requires credentials)"""
    print("\n🔹 EXAMPLE 4: With Authentication (requires credentials)")
    print("-" * 65)
    
    # Replace with your actual credentials or set as environment variables
    email = None  # Your Z-Library email
    password = None  # Your Z-Library password
    
    async with SimpleZLibrary(email, password) as zlib:
        # Get download limits
        limits = await zlib.get_limits()
        if limits:
            print("📊 Download Limits:")
            for key, value in limits.items():
                print(f"   {key}: {value}")
        
        # Search with authentication (may provide more results)
        results = await zlib.search("artificial intelligence", count=3)
        zlib.print_results(results)


async def example_multiple_searches():
    """Example: Multiple searches in one session"""
    print("\n🔹 EXAMPLE 5: Multiple Searches")
    print("-" * 35)
    
    async with SimpleZLibrary() as zlib:
        # Search for different topics
        topics = ["data science", "web development", "cybersecurity"]
        
        all_results = []
        for topic in topics:
            print(f"\n🔍 Searching for: {topic}")
            results = await zlib.search(topic, count=3)
            all_results.extend(results)
            
        # Save all results together
        zlib.save_results(all_results, "multiple_topics.json")
        print(f"\n📊 Total books found: {len(all_results)}")


async def main():
    """Run all examples"""
    print("🚀 Z-Library Simple Bot - Examples")
    print("=" * 50)
    
    try:
        # Run examples
        await example_basic_search()
        await example_advanced_search()
        await example_full_text_search()
        await example_with_authentication()
        await example_multiple_searches()
        
        print("\n✅ All examples completed!")
        print("📁 Check the 'zlibrary_output' folder for saved results")
        
    except Exception as e:
        print(f"❌ Error running examples: {e}")


if __name__ == "__main__":
    # Run the examples
    asyncio.run(main())