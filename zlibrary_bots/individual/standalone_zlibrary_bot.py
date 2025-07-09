#!/usr/bin/env python3
"""
Standalone Z-Library Bot
Individual implementation - works independently without integration
"""

import asyncio
import json
import os
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional

# Check zlibrary availability
try:
    import zlibrary
    from zlibrary import Language, Extension
    ZLIBRARY_AVAILABLE = True
except ImportError:
    print("❌ zlibrary not installed. Run: pip install zlibrary")
    ZLIBRARY_AVAILABLE = False
    exit(1)


class StandaloneZLibraryBot:
    """Individual Z-Library bot - works independently"""
    
    def __init__(self, email: Optional[str] = None, password: Optional[str] = None):
        """Initialize standalone bot"""
        self.email = email
        self.password = password
        self.lib = None
        self.authenticated = False
        
        # Create output directories
        self.setup_directories()
        
    def setup_directories(self):
        """Setup output directories"""
        self.base_dir = Path("standalone_zlibrary")
        self.base_dir.mkdir(exist_ok=True)
        
        (self.base_dir / "search_results").mkdir(exist_ok=True)
        (self.base_dir / "books").mkdir(exist_ok=True)
        (self.base_dir / "covers").mkdir(exist_ok=True)
        
        print(f"📁 Output directory: {self.base_dir}")
    
    async def connect(self):
        """Connect to Z-Library"""
        print("🔗 Connecting to Z-Library...")
        
        try:
            self.lib = zlibrary.AsyncZlib()
            
            if self.email and self.password:
                await self.lib.login(self.email, self.password)
                self.authenticated = True
                print("✅ Authenticated successfully")
            else:
                print("ℹ️ Running without authentication")
            
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    async def search_books(self, query: str, count: int = 10) -> List[Dict]:
        """Search for books"""
        print(f"\n🔍 Searching: '{query}'")
        
        try:
            paginator = await self.lib.search(q=query, count=count)
            results = await paginator.next()
            
            print(f"✅ Found {len(results)} results")
            return results
            
        except Exception as e:
            print(f"❌ Search failed: {e}")
            return []
    
    async def search_with_filters(self, 
                                query: str,
                                count: int = 10,
                                from_year: Optional[int] = None,
                                to_year: Optional[int] = None,
                                language: Optional[str] = None,
                                file_format: Optional[str] = None) -> List[Dict]:
        """Search with filters"""
        print(f"\n🎯 Filtered search: '{query}'")
        
        try:
            search_params = {'q': query, 'count': count}
            
            if from_year:
                search_params['from_year'] = from_year
            if to_year:
                search_params['to_year'] = to_year
                
            # Language filter
            if language:
                lang_map = {
                    'english': Language.ENGLISH,
                    'russian': Language.RUSSIAN,
                    'german': Language.GERMAN,
                    'french': Language.FRENCH,
                    'spanish': Language.SPANISH
                }
                if language.lower() in lang_map:
                    search_params['lang'] = [lang_map[language.lower()]]
            
            # Format filter
            if file_format:
                format_map = {
                    'pdf': Extension.PDF,
                    'epub': Extension.EPUB,
                    'mobi': Extension.MOBI,
                    'txt': Extension.TXT,
                    'doc': Extension.DOC
                }
                if file_format.lower() in format_map:
                    search_params['extensions'] = [format_map[file_format.lower()]]
            
            paginator = await self.lib.search(**search_params)
            results = await paginator.next()
            
            print(f"✅ Found {len(results)} filtered results")
            return results
            
        except Exception as e:
            print(f"❌ Filtered search failed: {e}")
            return []
    
    def save_results(self, results: List[Dict], filename: Optional[str] = None):
        """Save search results"""
        if not results:
            print("No results to save")
            return
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"search_{timestamp}.json"
        
        output_file = self.base_dir / "search_results" / filename
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved: {output_file}")
        return output_file
    
    def display_results(self, results: List[Dict], max_show: int = 10):
        """Display search results"""
        if not results:
            print("No results to display")
            return
        
        print(f"\n📚 Showing {min(len(results), max_show)} of {len(results)} results:")
        print("=" * 80)
        
        for i, book in enumerate(results[:max_show], 1):
            authors = book.get('authors', [])
            author_names = ", ".join([a.get('author', 'Unknown') for a in authors])
            
            print(f"\n{i}. {book.get('name', 'Unknown Title')}")
            print(f"   👤 Authors: {author_names}")
            print(f"   📅 Year: {book.get('year', 'Unknown')}")
            print(f"   📄 Format: {book.get('extension', 'Unknown')}")
            print(f"   📏 Size: {book.get('size', 'Unknown')}")
            print(f"   ⭐ Rating: {book.get('rating', 'No rating')}")
            if book.get('publisher'):
                print(f"   🏢 Publisher: {book.get('publisher')}")
            print(f"   🔗 URL: {book.get('url', 'N/A')}")
    
    async def get_download_limits(self):
        """Get download limits (requires authentication)"""
        if not self.authenticated:
            print("⚠️ Authentication required for download limits")
            return None
        
        try:
            limits = await self.lib.profile.get_limits()
            return limits
        except Exception as e:
            print(f"❌ Failed to get limits: {e}")
            return None
    
    def create_summary_report(self, all_results: Dict[str, List[Dict]]):
        """Create a summary report of all searches"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = self.base_dir / f"summary_report_{timestamp}.txt"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write("Z-Library Standalone Bot - Search Summary Report\n")
            f.write("=" * 60 + "\n")
            f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            total_books = 0
            for search_term, results in all_results.items():
                f.write(f"Search: '{search_term}'\n")
                f.write(f"Results: {len(results)} books\n")
                f.write("-" * 40 + "\n")
                
                for i, book in enumerate(results[:5], 1):  # Top 5 per search
                    authors = ", ".join([a.get('author', 'Unknown') for a in book.get('authors', [])])
                    f.write(f"  {i}. {book.get('name', 'Unknown')}\n")
                    f.write(f"     Author: {authors}\n")
                    f.write(f"     Year: {book.get('year', 'Unknown')}\n")
                    f.write(f"     Format: {book.get('extension', 'Unknown')}\n\n")
                
                total_books += len(results)
                f.write("\n")
            
            f.write(f"Total searches: {len(all_results)}\n")
            f.write(f"Total books found: {total_books}\n")
        
        print(f"📊 Summary report saved: {report_file}")
        return report_file


async def main():
    """Main function for standalone bot"""
    print("🚀 Standalone Z-Library Bot")
    print("=" * 40)
    
    # Initialize bot
    email = None  # Set your email here if you have account
    password = None  # Set your password here if you have account
    
    bot = StandaloneZLibraryBot(email, password)
    
    # Connect
    if not await bot.connect():
        print("❌ Failed to connect. Exiting.")
        return
    
    # Example searches
    search_queries = [
        "python programming",
        "machine learning",
        "data science",
        "artificial intelligence",
        "web development"
    ]
    
    all_results = {}
    
    try:
        print("\n🔍 Running example searches...")
        
        for query in search_queries:
            # Basic search
            results = await bot.search_books(query, count=5)
            if results:
                all_results[query] = results
                bot.display_results(results, max_show=3)
                
                # Save individual results
                filename = f"{query.replace(' ', '_')}_results.json"
                bot.save_results(results, filename)
        
        # Advanced search example
        print("\n🎯 Advanced search example...")
        advanced_results = await bot.search_with_filters(
            query="programming",
            count=3,
            from_year=2020,
            language="english",
            file_format="pdf"
        )
        
        if advanced_results:
            bot.display_results(advanced_results)
            bot.save_results(advanced_results, "advanced_search_results.json")
            all_results["advanced_programming"] = advanced_results
        
        # Show download limits if authenticated
        if bot.authenticated:
            print("\n📊 Download limits:")
            limits = await bot.get_download_limits()
            if limits:
                for key, value in limits.items():
                    print(f"   {key}: {value}")
        
        # Create summary report
        if all_results:
            bot.create_summary_report(all_results)
            
            print(f"\n✅ Completed! Found {sum(len(results) for results in all_results.values())} total books")
            print(f"📁 All files saved in: {bot.base_dir}")
            
            # List generated files
            print("\n📄 Generated files:")
            for file in bot.base_dir.rglob("*"):
                if file.is_file():
                    print(f"   📄 {file.relative_to(bot.base_dir)}")
        
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")


# Interactive mode
async def interactive_mode():
    """Interactive mode for manual searches"""
    print("🎮 Interactive Mode")
    print("=" * 30)
    
    bot = StandaloneZLibraryBot()
    
    if not await bot.connect():
        print("❌ Failed to connect")
        return
    
    while True:
        print("\n" + "="*40)
        print("1. Basic search")
        print("2. Advanced search")
        print("3. Show download limits")
        print("4. Exit")
        
        try:
            choice = input("\nChoose option (1-4): ").strip()
            
            if choice == "1":
                query = input("Enter search query: ").strip()
                count = int(input("Number of results (default 10): ").strip() or 10)
                
                results = await bot.search_books(query, count)
                bot.display_results(results)
                
                if results and input("Save results? (y/n): ").lower() == 'y':
                    filename = f"{query.replace(' ', '_')}_manual.json"
                    bot.save_results(results, filename)
            
            elif choice == "2":
                query = input("Enter search query: ").strip()
                count = int(input("Number of results (default 10): ").strip() or 10)
                
                from_year = input("From year (optional): ").strip()
                to_year = input("To year (optional): ").strip()
                language = input("Language (english/russian/etc, optional): ").strip()
                file_format = input("Format (pdf/epub/etc, optional): ").strip()
                
                results = await bot.search_with_filters(
                    query=query,
                    count=count,
                    from_year=int(from_year) if from_year else None,
                    to_year=int(to_year) if to_year else None,
                    language=language if language else None,
                    file_format=file_format if file_format else None
                )
                
                bot.display_results(results)
                
                if results and input("Save results? (y/n): ").lower() == 'y':
                    filename = f"{query.replace(' ', '_')}_filtered.json"
                    bot.save_results(results, filename)
            
            elif choice == "3":
                limits = await bot.get_download_limits()
                if limits:
                    print("\n📊 Download Limits:")
                    for key, value in limits.items():
                        print(f"   {key}: {value}")
                else:
                    print("⚠️ No limits available (authentication required)")
            
            elif choice == "4":
                print("👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid choice")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "interactive":
        asyncio.run(interactive_mode())
    else:
        asyncio.run(main())