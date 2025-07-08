#!/usr/bin/env python3
"""
Quick Start Script for Book Scraping Bot
Perfect for first-time users to test the bot
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

def quick_demo():
    """Run a quick demo of the bot"""
    print("🚀 Book Scraping Bot - Quick Start Demo")
    print("=" * 50)
    print()
    
    try:
        from main import BookScrapingBot
        from config.settings import settings
        
        # Show current configuration
        print("⚙️ Current Configuration:")
        print(f"   📁 Output directory: {settings.OUTPUT_DIR}")
        print(f"   📚 Download books: {settings.DOWNLOAD_BOOKS}")
        print(f"   🖼️ Download covers: {settings.DOWNLOAD_COVERS}")
        print(f"   💎 Premium tier: {settings.IS_PREMIUM}")
        print(f"   🚦 Rate limit: {settings.requests_per_minute} req/min")
        print()
        
        # Create bot
        print("🤖 Initializing bot...")
        bot = BookScrapingBot()
        
        # Quick search demo
        query = "python programming"
        print(f"🔍 Searching for: '{query}' (limited to 3 results)")
        print("⏳ This may take a few moments...")
        print()
        
        # Search with limited results for demo
        results = bot.search_and_process(query, limit=3, download=False)
        
        if results:
            print(f"✅ Found {len(results)} books!")
            print()
            print("📚 Results Preview:")
            print("-" * 40)
            
            for i, book in enumerate(results, 1):
                print(f"\n{i}. 📖 {book.title}")
                print(f"   👤 Author: {book.author}")
                print(f"   📅 Year: {book.year or 'Unknown'}")
                print(f"   📄 Format: {book.file_format or 'Unknown'}")
                print(f"   💾 Size: {book.file_size or 'Unknown'}")
                print(f"   🔗 Source: {book.source}")
                if book.download_url:
                    print(f"   📥 Download available: Yes")
                else:
                    print(f"   📥 Download available: No")
            
            # Show what files were generated
            print("\n📁 Generated Files:")
            output_path = Path(settings.OUTPUT_DIR)
            
            # Check for JSON files
            json_files = list((output_path / "metadata").glob("*.json"))
            if json_files:
                print(f"   📝 {len(json_files)} JSON metadata files")
            
            # Check for CSV files
            csv_files = list((output_path / "metadata").glob("*.csv"))
            if csv_files:
                print(f"   📊 {len(csv_files)} CSV files")
            
            # Check for HTML files
            html_files = list((output_path / "html").glob("*.html"))
            if html_files:
                print(f"   🌐 {len(html_files)} HTML pages")
            
            print(f"\n📂 Check the '{settings.OUTPUT_DIR}' folder for all generated files!")
            
        else:
            print("❌ No books found. This might be due to:")
            print("   - Network connectivity issues")
            print("   - Source websites being temporarily unavailable")
            print("   - Rate limiting (try again in a few minutes)")
        
        # Show next steps
        print("\n🎯 Next Steps:")
        print("1. 📖 Read USAGE.md for detailed instructions")
        print("2. ⚙️ Edit .env file to configure API keys and settings")
        print("3. 🔍 Try more searches:")
        print("   python main.py search 'machine learning' --limit 5")
        print("   python main.py book 'Clean Code' --author 'Robert Martin'")
        print("4. 📊 Check statistics: python main.py stats")
        print("5. 🧪 Run full examples: python run_example.py")
        
        # Premium features teaser
        print("\n💎 Premium Features Available:")
        print("   🎥 Video generation for social media")
        print("   🤖 Telegram bot notifications")
        print("   📈 Advanced analytics and reporting")
        print("   ⚡ Unlimited concurrent downloads")
        print("   🎯 Priority support and custom features")
        
        bot.close()
        print("\n✅ Demo completed successfully!")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Try running: pip install -r requirements.txt")
        return False
        
    except Exception as e:
        print(f"❌ Error during demo: {e}")
        print("💡 Try running: python test_bot.py")
        return False
    
    return True

def show_help():
    """Show help information"""
    print("📚 Book Scraping Bot - Quick Start Help")
    print("=" * 50)
    print()
    print("🎯 Available Commands:")
    print()
    print("Basic Usage:")
    print("  python quick_start.py          # Run this demo")
    print("  python main.py search 'query'  # Search for books")
    print("  python main.py stats           # Show statistics")
    print("  python main.py config          # Show configuration")
    print()
    print("Examples:")
    print("  python main.py search 'python programming' --limit 5")
    print("  python main.py book 'Clean Code' --author 'Robert Martin'")
    print("  python main.py search 'algorithms' --source libgen")
    print()
    print("Testing:")
    print("  python test_bot.py             # Run test suite")
    print("  python setup.py               # Setup/reinstall")
    print("  python run_example.py         # Advanced examples")
    print()
    print("📖 Documentation:")
    print("  README.md     - Installation and overview")
    print("  USAGE.md      - Detailed usage guide") 
    print("  FEATURES.md   - Complete feature list")
    print("  .env.example  - Configuration reference")

def main():
    """Main function"""
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        if arg in ['help', '-h', '--help']:
            show_help()
            return
        elif arg in ['demo', 'run', 'start']:
            quick_demo()
            return
    
    # Default: run demo
    print("💡 Running quick demo. Use 'python quick_start.py help' for more options.")
    print()
    quick_demo()

if __name__ == "__main__":
    main()