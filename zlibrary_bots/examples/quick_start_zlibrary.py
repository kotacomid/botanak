#!/usr/bin/env python3
"""
Quick Start Z-Library Bot
Simple demonstration of Z-Library functionality
"""

import asyncio
import json
from pathlib import Path

try:
    import zlibrary
    from zlibrary import Language, Extension
    ZLIBRARY_AVAILABLE = True
except ImportError:
    print("⚠️ zlibrary package not installed.")
    print("To install: pip install zlibrary")
    ZLIBRARY_AVAILABLE = False


async def quick_search_demo():
    """Quick search demonstration"""
    if not ZLIBRARY_AVAILABLE:
        print("Cannot run demo without zlibrary package.")
        return
    
    print("🚀 Z-Library Quick Start Demo")
    print("=" * 40)
    
    # Initialize Z-Library
    lib = zlibrary.AsyncZlib()
    
    try:
        print("📚 Searching for 'Python Programming' books...")
        
        # Basic search
        paginator = await lib.search(q="Python Programming", count=5)
        results = await paginator.next()
        
        print(f"✅ Found {len(results)} books!")
        print("\n📖 Results:")
        print("-" * 50)
        
        # Display results
        for i, book in enumerate(results, 1):
            authors = book.get('authors', [])
            author_names = ", ".join([author.get('author', 'Unknown') for author in authors])
            
            print(f"{i}. {book.get('name', 'Unknown Title')}")
            print(f"   👤 Author: {author_names}")
            print(f"   📅 Year: {book.get('year', 'Unknown')}")
            print(f"   📄 Format: {book.get('extension', 'Unknown')}")
            print(f"   📏 Size: {book.get('size', 'Unknown')}")
            print(f"   ⭐ Rating: {book.get('rating', 'No rating')}")
            print()
        
        # Save results
        output_dir = Path("zlibrary_output")
        output_dir.mkdir(exist_ok=True)
        
        output_file = output_dir / "quick_demo_results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        print(f"💾 Results saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("This might be due to network issues or Z-Library being unavailable.")


async def advanced_search_demo():
    """Advanced search with filters"""
    if not ZLIBRARY_AVAILABLE:
        return
    
    print("\n🔍 Advanced Search Demo")
    print("=" * 30)
    
    lib = zlibrary.AsyncZlib()
    
    try:
        print("📚 Searching for recent Machine Learning books in English PDF format...")
        
        # Advanced search with filters
        paginator = await lib.search(
            q="Machine Learning",
            count=3,
            from_year=2020,
            to_year=2024,
            lang=[Language.ENGLISH],
            extensions=[Extension.PDF]
        )
        
        results = await paginator.next()
        
        print(f"✅ Found {len(results)} filtered results!")
        
        for i, book in enumerate(results, 1):
            print(f"\n{i}. {book.get('name', 'Unknown')}")
            print(f"   📅 Year: {book.get('year', 'Unknown')}")
            print(f"   🌐 Language: {book.get('language', 'Unknown')}")
            print(f"   📄 Format: {book.get('extension', 'Unknown')}")
        
    except Exception as e:
        print(f"❌ Advanced search error: {e}")


def print_usage_info():
    """Print usage information"""
    print("\n📋 Usage Information")
    print("=" * 25)
    print("This demo shows basic Z-Library functionality.")
    print()
    print("🔧 To use with authentication:")
    print("   lib = zlibrary.AsyncZlib()")
    print("   await lib.login('your_email', 'your_password')")
    print()
    print("🔒 For privacy with Tor:")
    print("   lib = zlibrary.AsyncZlib(onion=True, proxy_list=['socks5://127.0.0.1:9050'])")
    print()
    print("📖 Available search options:")
    print("   - Basic search: lib.search(q='query', count=10)")
    print("   - With filters: lib.search(q='query', from_year=2020, lang=[Language.ENGLISH])")
    print("   - Full-text: lib.full_text_search(q='text to find in books')")
    print()
    print("🌐 Supported languages: English, Russian, German, French, Spanish, etc.")
    print("📄 Supported formats: PDF, EPUB, MOBI, AZW, FB2, TXT, DOC, etc.")


async def main():
    """Main demo function"""
    print("🎯 Z-Library Simple Bot Demo")
    print("============================")
    
    if not ZLIBRARY_AVAILABLE:
        print("\n❌ Cannot run demo - zlibrary package not installed")
        print("To install: pip install zlibrary")
        print("\nExample of what the demo would show:")
        print("- Basic book search")
        print("- Advanced search with filters") 
        print("- Result display and saving")
        return
    
    try:
        # Run demos
        await quick_search_demo()
        await advanced_search_demo()
        
        # Print usage info
        print_usage_info()
        
        print("\n✅ Demo completed successfully!")
        print("📁 Check 'zlibrary_output' folder for saved results")
        
    except KeyboardInterrupt:
        print("\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")


if __name__ == "__main__":
    asyncio.run(main())