#!/usr/bin/env python3
"""
Fixed Z-Library Example Script
This version has better error handling and should work with installed zlibrary package
"""

import asyncio
import json
from pathlib import Path
from typing import List, Dict, Optional

def check_zlibrary_import():
    """Check if zlibrary can be imported and return status"""
    try:
        import zlibrary
        from zlibrary import Language, Extension
        print("✅ zlibrary package imported successfully")
        return True, zlibrary, Language, Extension
    except ImportError as e:
        print(f"❌ zlibrary import failed: {e}")
        print("💡 Try: pip install --force-reinstall zlibrary")
        return False, None, None, None
    except Exception as e:
        print(f"❌ Unexpected error importing zlibrary: {e}")
        return False, None, None, None

class FixedZLibrary:
    """Fixed Z-Library interface with better error handling"""
    
    def __init__(self, email: Optional[str] = None, password: Optional[str] = None):
        """Initialize with optional credentials"""
        self.email = email
        self.password = password
        self.lib = None
        self.authenticated = False
        
        # Check imports
        self.available, self.zlibrary, self.Language, self.Extension = check_zlibrary_import()
        
    async def __aenter__(self):
        """Async context manager entry"""
        if self.available:
            await self.connect()
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit"""
        pass
        
    async def connect(self):
        """Connect to Z-Library"""
        if not self.available:
            print("❌ zlibrary package not available")
            return
            
        try:
            self.lib = self.zlibrary.AsyncZlib()
            
            if self.email and self.password:
                await self.lib.login(self.email, self.password)
                self.authenticated = True
                print("✅ Successfully logged in to Z-Library")
            else:
                print("ℹ️ Running without authentication (limited features)")
                
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            
    async def search(self, query: str, count: int = 10) -> List[Dict]:
        """Search for books"""
        if not self.available or not self.lib:
            print("❌ Z-Library not available or not connected")
            return []
            
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
        """Advanced search with filters"""
        if not self.available or not self.lib:
            print("❌ Z-Library not available or not connected")
            return []
            
        print(f"🔍 Advanced search for: {query}")
        
        try:
            # Build search parameters
            search_params = {'q': query, 'count': count}
            
            if from_year:
                search_params['from_year'] = from_year
            if to_year:
                search_params['to_year'] = to_year
            
            # Convert language filter (using getattr to safely access enums)
            if language and self.Language:
                lang_mapping = {
                    'english': getattr(self.Language, 'ENGLISH', None),
                    'russian': getattr(self.Language, 'RUSSIAN', None),
                    'german': getattr(self.Language, 'GERMAN', None),
                    'french': getattr(self.Language, 'FRENCH', None),
                    'spanish': getattr(self.Language, 'SPANISH', None),
                    'italian': getattr(self.Language, 'ITALIAN', None),
                    'chinese': getattr(self.Language, 'CHINESE', None),
                    'japanese': getattr(self.Language, 'JAPANESE', None)
                }
                lang_enum = lang_mapping.get(language.lower())
                if lang_enum:
                    search_params['lang'] = [lang_enum]
            
            # Convert format filter
            if file_format and self.Extension:
                ext_mapping = {
                    'pdf': getattr(self.Extension, 'PDF', None),
                    'epub': getattr(self.Extension, 'EPUB', None),
                    'mobi': getattr(self.Extension, 'MOBI', None),
                    'azw': getattr(self.Extension, 'AZW', None),
                    'azw3': getattr(self.Extension, 'AZW3', None),
                    'fb2': getattr(self.Extension, 'FB2', None),
                    'txt': getattr(self.Extension, 'TXT', None),
                    'rtf': getattr(self.Extension, 'RTF', None),
                    'doc': getattr(self.Extension, 'DOC', None),
                    'docx': getattr(self.Extension, 'DOCX', None)
                }
                ext_enum = ext_mapping.get(file_format.lower())
                if ext_enum:
                    search_params['extensions'] = [ext_enum]
            
            paginator = await self.lib.search(**search_params)
            results = await paginator.next()
            
            print(f"✅ Found {len(results)} books with filters")
            return results
            
        except Exception as e:
            print(f"❌ Advanced search failed: {e}")
            return []
    
    def save_results(self, results: List[Dict], filename: str = "zlibrary_results.json"):
        """Save search results to JSON file"""
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
        """Print search results in a nice format"""
        if not results:
            print("No results to display")
            return
            
        print(f"\n📚 Showing {min(len(results), max_results)} of {len(results)} results:")
        print("=" * 80)
        
        for i, book in enumerate(results[:max_results], 1):
            authors = book.get('authors', [])
            author_names = ", ".join([author.get('author', 'Unknown') for author in authors])
            
            print(f"\n{i}. {book.get('name', 'Unknown Title')}")
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
    
    async with FixedZLibrary() as zlib:
        if not zlib.available:
            print("❌ Cannot run example - zlibrary not available")
            return
            
        # Search for programming books
        results = await zlib.search("python programming", count=5)
        zlib.print_results(results)
        if results:
            zlib.save_results(results, "python_books.json")


async def example_advanced_search():
    """Example: Advanced search with filters"""
    print("\n🔹 EXAMPLE 2: Advanced Search with Filters")
    print("-" * 50)
    
    async with FixedZLibrary() as zlib:
        if not zlib.available:
            print("❌ Cannot run example - zlibrary not available")
            return
            
        # Search for recent books in PDF format
        results = await zlib.search_advanced(
            query="machine learning",
            count=5,
            from_year=2020,
            to_year=2024,
            language="english",
            file_format="pdf"
        )
        zlib.print_results(results)


async def example_with_authentication():
    """Example: Using with authentication (requires credentials)"""
    print("\n🔹 EXAMPLE 3: With Authentication (requires credentials)")
    print("-" * 65)
    
    # Replace with your actual credentials or set as environment variables
    email = None  # Your Z-Library email
    password = None  # Your Z-Library password
    
    async with FixedZLibrary(email, password) as zlib:
        if not zlib.available:
            print("❌ Cannot run example - zlibrary not available")
            return
            
        # Search with authentication (may provide more results)
        results = await zlib.search("artificial intelligence", count=3)
        zlib.print_results(results)


async def main():
    """Run all examples"""
    print("🚀 Fixed Z-Library Examples")
    print("=" * 50)
    
    try:
        # Check zlibrary availability first
        available, _, _, _ = check_zlibrary_import()
        
        if not available:
            print("\n❌ zlibrary package is not working properly")
            print("\n💡 Suggested solutions:")
            print("1. pip install --force-reinstall zlibrary")
            print("2. pip uninstall zlibrary && pip install zlibrary")
            print("3. Check Python environment: which python && which pip")
            print("4. Try: python -c \"import zlibrary; print('Success')\"")
            return
        
        # Run examples
        await example_basic_search()
        await example_advanced_search()
        await example_with_authentication()
        
        print("\n✅ All examples completed!")
        print("📁 Check the 'zlibrary_output' folder for saved results")
        
    except KeyboardInterrupt:
        print("\n🛑 Examples interrupted by user")
    except Exception as e:
        print(f"\n❌ Error running examples: {e}")
        print("\n💡 Try running the diagnostic script: python diagnose_zlibrary.py")


if __name__ == "__main__":
    asyncio.run(main())