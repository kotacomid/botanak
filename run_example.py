#!/usr/bin/env python3
"""
Example script showing how to use the Book Scraping Bot
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from main import BookScrapingBot
from config.settings import settings

def basic_example():
    """Basic usage example"""
    print("🚀 Starting Book Scraping Bot Example")
    print("=" * 50)
    
    # Create bot instance
    bot = BookScrapingBot()
    
    try:
        # Search for books
        query = "clean code"
        print(f"🔍 Searching for: {query}")
        
        results = bot.search_and_process(query, limit=5, download=True)
        
        if results:
            print(f"\n✅ Found {len(results)} books!")
            print("\n📚 Results:")
            print("-" * 30)
            
            for i, book in enumerate(results, 1):
                print(f"{i}. {book.title}")
                print(f"   Author: {book.author}")
                print(f"   Format: {book.file_format}")
                print(f"   Source: {book.source}")
                if book.local_file_path:
                    print(f"   ✅ Downloaded: {Path(book.local_file_path).name}")
                print()
        else:
            print("❌ No books found")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        bot.close()
        print("👋 Bot closed")

def advanced_example():
    """Advanced usage with specific configuration"""
    print("🚀 Advanced Book Scraping Example")
    print("=" * 50)
    
    # Create bot
    bot = BookScrapingBot()
    
    try:
        # Search multiple books
        books_to_search = [
            "python programming",
            "machine learning",
            "data structures algorithms"
        ]
        
        all_results = []
        
        for query in books_to_search:
            print(f"\n🔍 Searching: {query}")
            results = bot.search_and_process(query, limit=3, download=False)
            all_results.extend(results)
        
        print(f"\n📊 Total books found: {len(all_results)}")
        
        # Show statistics
        stats = bot.get_stats()
        print(f"🎯 Tier: {stats['tier']}")
        print(f"📥 Books downloaded: {stats['downloads']['books_downloaded']}")
        print(f"🖼️ Covers downloaded: {stats['downloads']['covers_downloaded']}")
        
        # Display enabled features
        features = stats['features']
        print("\n🔧 Enabled features:")
        for feature, enabled in features.items():
            status = "✅" if enabled else "❌"
            print(f"  {status} {feature.replace('_', ' ').title()}")
    
    except Exception as e:
        print(f"❌ Error: {e}")
        
    finally:
        bot.close()

def search_specific_book():
    """Search for a specific book by title and author"""
    print("🎯 Specific Book Search Example")
    print("=" * 50)
    
    bot = BookScrapingBot()
    
    try:
        # Search for specific book
        title = "Clean Code"
        author = "Robert Martin"
        
        print(f"📖 Looking for: '{title}' by {author}")
        
        results = bot.scraper.search_book(title, author)
        
        if results:
            book = results[0]  # Take first result
            print(f"\n✅ Found: {book.title}")
            print(f"📝 Author: {book.author}")
            print(f"📅 Year: {book.year}")
            print(f"📄 Format: {book.file_format}")
            print(f"💾 Size: {book.file_size}")
            print(f"🔗 Source: {book.source}")
            
            # Download if available
            if book.download_url and settings.DOWNLOAD_BOOKS:
                print(f"\n📥 Downloading...")
                file_path = bot.downloader.download_book(book)
                if file_path:
                    print(f"✅ Downloaded to: {file_path}")
                else:
                    print("❌ Download failed")
        else:
            print("❌ Book not found")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        bot.close()

async def async_download_example():
    """Example of asynchronous downloading"""
    print("⚡ Async Download Example")
    print("=" * 50)
    
    bot = BookScrapingBot()
    
    try:
        # Search for multiple books
        results = bot.search_and_process("programming", limit=5, download=False)
        
        if results:
            print(f"🔍 Found {len(results)} books")
            print("📥 Starting async downloads...")
            
            # Download asynchronously
            download_results = await bot.downloader.download_multiple_async(results)
            
            print("\n📊 Download Results:")
            for title, result in download_results.items():
                book_status = "✅" if result.get('book_path') else "❌"
                cover_status = "✅" if result.get('cover_path') else "❌"
                print(f"  📚 {book_status} 🖼️ {cover_status} {title[:50]}...")
        
        else:
            print("❌ No books found")
    
    except Exception as e:
        print(f"❌ Error: {e}")
    
    finally:
        bot.close()

def configuration_example():
    """Show configuration and validation"""
    print("⚙️ Configuration Example")
    print("=" * 50)
    
    # Show current settings
    print(f"🎯 Premium tier: {settings.IS_PREMIUM}")
    print(f"📥 Download books: {settings.DOWNLOAD_BOOKS}")
    print(f"🖼️ Download covers: {settings.DOWNLOAD_COVERS}")
    print(f"💾 Max file size: {settings.MAX_FILE_SIZE_MB} MB")
    print(f"⏱️ Scraping delay: {settings.SCRAPING_DELAY}s")
    print(f"🚦 Rate limit: {settings.requests_per_minute} req/min")
    
    # Show enabled features
    features = settings.get_enabled_features()
    print(f"\n🔧 Features ({len([f for f in features.values() if f])} enabled):")
    for feature, enabled in features.items():
        status = "✅" if enabled else "❌"
        print(f"  {status} {feature.replace('_', ' ').title()}")

def main():
    """Main function to run examples"""
    print("📚 Book Scraping Bot - Examples")
    print("=" * 60)
    
    examples = {
        '1': ('Basic Search & Download', basic_example),
        '2': ('Advanced Multi-Search', advanced_example),
        '3': ('Specific Book Search', search_specific_book),
        '4': ('Async Downloads', lambda: asyncio.run(async_download_example())),
        '5': ('Show Configuration', configuration_example),
    }
    
    print("\nChoose an example to run:")
    for key, (name, _) in examples.items():
        print(f"  {key}. {name}")
    
    choice = input("\nEnter choice (1-5) or press Enter for basic example: ").strip()
    
    if not choice:
        choice = '1'
    
    if choice in examples:
        name, func = examples[choice]
        print(f"\n🚀 Running: {name}")
        print("=" * 60)
        func()
    else:
        print("❌ Invalid choice")

if __name__ == "__main__":
    main()