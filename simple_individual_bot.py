#!/usr/bin/env python3
"""
Simple Individual Z-Library Bot
Easy to use, focused implementation
"""

import asyncio
import json
from pathlib import Path
from datetime import datetime

def check_zlibrary():
    """Check if zlibrary is available"""
    try:
        import zlibrary
        return True, zlibrary
    except ImportError:
        print("❌ zlibrary not installed")
        print("Install with: pip install zlibrary")
        return False, None

class SimpleZBot:
    """Simple individual Z-Library bot"""
    
    def __init__(self):
        """Initialize simple bot"""
        self.available, self.zlibrary = check_zlibrary()
        self.lib = None
        self.output_dir = Path("simple_zbot_output")
        self.output_dir.mkdir(exist_ok=True)
        
        print(f"📁 Output: {self.output_dir}")
    
    async def connect(self, email=None, password=None):
        """Connect to Z-Library"""
        if not self.available:
            print("❌ Cannot connect - zlibrary not available")
            return False
        
        try:
            self.lib = self.zlibrary.AsyncZlib()
            
            if email and password:
                await self.lib.login(email, password)
                print("✅ Logged in successfully")
            else:
                print("ℹ️ Connected without login")
            
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    async def search(self, query, count=10):
        """Simple search"""
        if not self.lib:
            print("❌ Not connected")
            return []
        
        print(f"🔍 Searching: {query}")
        
        try:
            paginator = await self.lib.search(q=query, count=count)
            results = await paginator.next()
            
            print(f"✅ Found {len(results)} books")
            return results
            
        except Exception as e:
            print(f"❌ Search failed: {e}")
            return []
    
    def save(self, results, name="search_results"):
        """Save results to JSON"""
        if not results:
            print("No results to save")
            return
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.json"
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Saved: {filepath}")
        return filepath
    
    def show(self, results, max_items=5):
        """Display results nicely"""
        if not results:
            print("No results to show")
            return
        
        print(f"\n📚 Showing {min(len(results), max_items)} of {len(results)} results:")
        print("-" * 60)
        
        for i, book in enumerate(results[:max_items], 1):
            title = book.get('name', 'Unknown Title')
            authors = book.get('authors', [])
            author_names = ", ".join([a.get('author', 'Unknown') for a in authors])
            year = book.get('year', 'Unknown')
            format_type = book.get('extension', 'Unknown')
            size = book.get('size', 'Unknown')
            
            print(f"\n{i}. {title}")
            print(f"   Author: {author_names}")
            print(f"   Year: {year} | Format: {format_type} | Size: {size}")
            
            if book.get('url'):
                print(f"   URL: {book.get('url')}")


async def quick_demo():
    """Quick demonstration"""
    print("🚀 Simple Z-Library Bot Demo")
    print("=" * 40)
    
    # Create bot
    bot = SimpleZBot()
    
    # Connect (without login for demo)
    if not await bot.connect():
        return
    
    # Example searches
    searches = [
        ("python programming", 3),
        ("machine learning", 3),
        ("web development", 3)
    ]
    
    all_results = []
    
    for query, count in searches:
        results = await bot.search(query, count)
        if results:
            bot.show(results, max_items=2)
            bot.save(results, query.replace(' ', '_'))
            all_results.extend(results)
    
    print(f"\n✅ Demo completed!")
    print(f"📚 Total books found: {len(all_results)}")
    print(f"📁 Files saved in: {bot.output_dir}")


async def interactive():
    """Interactive mode"""
    print("🎮 Interactive Z-Library Search")
    print("=" * 35)
    
    bot = SimpleZBot()
    
    # Get login info
    print("\nLogin (optional - press Enter to skip):")
    email = input("Email: ").strip() or None
    password = input("Password: ").strip() or None
    
    if not await bot.connect(email, password):
        return
    
    while True:
        print("\n" + "="*30)
        query = input("Search query (or 'quit' to exit): ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not query:
            continue
        
        try:
            count = int(input("Number of results (default 10): ").strip() or 10)
        except ValueError:
            count = 10
        
        results = await bot.search(query, count)
        
        if results:
            bot.show(results)
            
            save_choice = input("\nSave results? (y/n): ").strip().lower()
            if save_choice == 'y':
                name = input("Filename (optional): ").strip() or query.replace(' ', '_')
                bot.save(results, name)


def main():
    """Main function"""
    print("🔷 Simple Individual Z-Library Bot")
    print("Choose mode:")
    print("1. Quick demo")
    print("2. Interactive search")
    
    choice = input("\nEnter choice (1 or 2): ").strip()
    
    if choice == "1":
        asyncio.run(quick_demo())
    elif choice == "2":
        asyncio.run(interactive())
    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    main()