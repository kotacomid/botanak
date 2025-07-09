#!/usr/bin/env python3
"""
Simple Z-Library Bot
Easy-to-use individual bot for quick searches
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
        print("Install: pip install --break-system-packages zlibrary")
        return False, None

class SimpleZBot:
    """Simple Z-Library bot"""
    
    def __init__(self):
        """Initialize bot"""
        self.available, self.zlibrary = check_zlibrary()
        self.lib = None
        self.output_dir = Path("simple_bot_results")
        self.output_dir.mkdir(exist_ok=True)
        
        if self.available:
            print("✅ Z-Library ready")
            print(f"📁 Output: {self.output_dir}")
        
    async def connect(self, email=None, password=None):
        """Connect to Z-Library"""
        if not self.available:
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
    
    def save(self, results, filename=None):
        """Save results"""
        if not results:
            return
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"search_{timestamp}.json"
        
        filepath = self.output_dir / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 Saved: {filepath}")
        return filepath
    
    def show(self, results, max_items=5):
        """Display results"""
        if not results:
            print("No results")
            return
        
        print(f"\n📚 {min(len(results), max_items)} of {len(results)} results:")
        print("-" * 50)
        
        for i, book in enumerate(results[:max_items], 1):
            title = book.get('name', 'Unknown')
            authors = book.get('authors', [])
            author_names = ", ".join([a.get('author', 'Unknown') for a in authors])
            year = book.get('year', 'Unknown')
            format_type = book.get('extension', 'Unknown')
            
            print(f"\n{i}. {title}")
            print(f"   Author: {author_names}")
            print(f"   Year: {year} | Format: {format_type}")


async def quick_demo():
    """Quick demo"""
    print("🚀 Simple Z-Library Bot Demo")
    print("=" * 35)
    
    bot = SimpleZBot()
    
    if not await bot.connect():
        return
    
    # Demo searches
    searches = ["python programming", "machine learning", "web development"]
    
    for query in searches:
        results = await bot.search(query, 3)
        if results:
            bot.show(results, 2)
            bot.save(results, f"{query.replace(' ', '_')}.json")
    
    print(f"\n✅ Demo completed! Check {bot.output_dir}")


async def interactive():
    """Interactive mode"""
    print("🎮 Interactive Z-Library Search")
    print("=" * 30)
    
    bot = SimpleZBot()
    
    # Optional login
    email = input("Email (optional): ").strip() or None
    password = input("Password (optional): ").strip() or None
    
    if not await bot.connect(email, password):
        return
    
    while True:
        print("\n" + "="*25)
        query = input("Search (or 'quit'): ").strip()
        
        if query.lower() in ['quit', 'exit', 'q']:
            print("👋 Goodbye!")
            break
        
        if not query:
            continue
        
        try:
            count = int(input("Results (default 10): ").strip() or 10)
        except ValueError:
            count = 10
        
        results = await bot.search(query, count)
        
        if results:
            bot.show(results)
            
            if input("Save? (y/n): ").lower() == 'y':
                name = input("Filename: ").strip() or None
                bot.save(results, name)


def main():
    """Main function"""
    print("🔷 Simple Z-Library Bot")
    print("1. Quick demo")
    print("2. Interactive search")
    
    choice = input("Choose (1 or 2): ").strip()
    
    if choice == "1":
        asyncio.run(quick_demo())
    elif choice == "2":
        asyncio.run(interactive())
    else:
        print("❌ Invalid choice")


if __name__ == "__main__":
    main()