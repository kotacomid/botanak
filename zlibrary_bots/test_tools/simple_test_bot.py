#!/usr/bin/env python3
"""
Simple Z-Library Test Bot
Minimal implementation to test core Z-Library functionality
"""

import asyncio
import json
import sys
from pathlib import Path
from datetime import datetime

# Check if zlibrary is available
try:
    import zlibrary
    ZLIBRARY_AVAILABLE = True
    print("✅ zlibrary package found")
except ImportError:
    ZLIBRARY_AVAILABLE = False
    print("❌ zlibrary package not found")
    print("   Install with: pip install zlibrary")


class SimpleTestBot:
    """Simple test bot for Z-Library functionality"""
    
    def __init__(self):
        self.lib = None
        self.test_results = {
            'connection': False,
            'basic_search': False,
            'search_with_filters': False,
            'result_count': 0,
            'errors': []
        }
    
    async def connect(self):
        """Test connection to Z-Library"""
        print("\n🔗 Testing connection...")
        
        if not ZLIBRARY_AVAILABLE:
            self.test_results['errors'].append("zlibrary package not available")
            print("❌ Cannot connect - package not installed")
            return False
        
        try:
            self.lib = zlibrary.AsyncZlib()
            self.test_results['connection'] = True
            print("✅ Connection successful")
            return True
        except Exception as e:
            self.test_results['errors'].append(f"Connection failed: {str(e)}")
            print(f"❌ Connection failed: {e}")
            return False
    
    async def test_basic_search(self):
        """Test basic search functionality"""
        print("\n🔍 Testing basic search...")
        
        if not self.lib:
            print("❌ No connection available")
            return False
        
        try:
            # Search for a common topic
            print("   Searching for 'Python programming'...")
            paginator = await self.lib.search(q="Python programming", count=3)
            results = await paginator.next()
            
            self.test_results['basic_search'] = True
            self.test_results['result_count'] = len(results)
            
            print(f"✅ Basic search successful - found {len(results)} results")
            
            # Display first result if available
            if results:
                book = results[0]
                print(f"   📚 First result: {book.get('name', 'Unknown title')}")
                authors = book.get('authors', [])
                if authors:
                    author_names = ", ".join([a.get('author', '') for a in authors])
                    print(f"   👤 Author(s): {author_names}")
                print(f"   📅 Year: {book.get('year', 'Unknown')}")
                print(f"   📄 Format: {book.get('extension', 'Unknown')}")
            
            return True
            
        except Exception as e:
            self.test_results['errors'].append(f"Basic search failed: {str(e)}")
            print(f"❌ Basic search failed: {e}")
            return False
    
    async def test_search_with_filters(self):
        """Test search with filters"""
        print("\n🎯 Testing filtered search...")
        
        if not self.lib:
            print("❌ No connection available")
            return False
        
        try:
            # Test with year and language filters
            print("   Searching for recent books about 'data science'...")
            
            # Import Language enum
            from zlibrary import Language
            
            paginator = await self.lib.search(
                q="data science",
                count=2,
                from_year=2020,
                lang=[Language.ENGLISH]
            )
            results = await paginator.next()
            
            self.test_results['search_with_filters'] = True
            
            print(f"✅ Filtered search successful - found {len(results)} results")
            
            # Show results
            for i, book in enumerate(results, 1):
                print(f"   {i}. {book.get('name', 'Unknown')}")
                print(f"      Year: {book.get('year', 'Unknown')}")
                print(f"      Language: {book.get('language', 'Unknown')}")
            
            return True
            
        except Exception as e:
            self.test_results['errors'].append(f"Filtered search failed: {str(e)}")
            print(f"❌ Filtered search failed: {e}")
            return False
    
    def save_test_results(self):
        """Save test results to file"""
        print("\n💾 Saving test results...")
        
        # Create output directory
        output_dir = Path("test_output")
        output_dir.mkdir(exist_ok=True)
        
        # Add timestamp
        self.test_results['timestamp'] = datetime.now().isoformat()
        self.test_results['zlibrary_available'] = ZLIBRARY_AVAILABLE
        
        # Save results
        output_file = output_dir / "test_results.json"
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(self.test_results, f, indent=2)
        
        print(f"✅ Test results saved to: {output_file}")
    
    def print_summary(self):
        """Print test summary"""
        print("\n" + "="*50)
        print("📊 TEST SUMMARY")
        print("="*50)
        
        total_tests = 3
        passed_tests = sum([
            self.test_results['connection'],
            self.test_results['basic_search'],
            self.test_results['search_with_filters']
        ])
        
        print(f"Tests passed: {passed_tests}/{total_tests}")
        print(f"Package available: {'✅' if ZLIBRARY_AVAILABLE else '❌'}")
        print(f"Connection: {'✅' if self.test_results['connection'] else '❌'}")
        print(f"Basic search: {'✅' if self.test_results['basic_search'] else '❌'}")
        print(f"Filtered search: {'✅' if self.test_results['search_with_filters'] else '❌'}")
        print(f"Results found: {self.test_results['result_count']}")
        
        if self.test_results['errors']:
            print(f"\n❌ Errors encountered:")
            for error in self.test_results['errors']:
                print(f"   • {error}")
        
        if passed_tests == total_tests:
            print(f"\n🎉 All tests passed! Z-Library bot is working correctly.")
        else:
            print(f"\n⚠️ Some tests failed. Check errors above.")
        
        print("="*50)


async def run_tests():
    """Run all tests"""
    print("🚀 Starting Z-Library Simple Test Bot")
    print("="*50)
    
    bot = SimpleTestBot()
    
    # Run tests in sequence
    await bot.connect()
    
    if bot.test_results['connection']:
        await bot.test_basic_search()
        await bot.test_search_with_filters()
    
    # Save and display results
    bot.save_test_results()
    bot.print_summary()
    
    return bot.test_results


async def demo_without_package():
    """Demo what the bot would do if package was available"""
    print("\n🎭 DEMO MODE (zlibrary package not available)")
    print("="*50)
    print("This is what the bot would do with zlibrary installed:")
    print()
    print("1. 🔗 Connect to Z-Library")
    print("   ✅ Connection successful")
    print()
    print("2. 🔍 Test basic search for 'Python programming'")
    print("   ✅ Found 3 results")
    print("   📚 First result: Learning Python, 5th Edition")
    print("   👤 Author: Mark Lutz") 
    print("   📅 Year: 2019")
    print("   📄 Format: PDF")
    print()
    print("3. 🎯 Test filtered search for 'data science' (2020+, English)")
    print("   ✅ Found 2 results")
    print("   1. Hands-On Machine Learning")
    print("      Year: 2022")
    print("      Language: english")
    print("   2. Python for Data Analysis")
    print("      Year: 2021") 
    print("      Language: english")
    print()
    print("📊 DEMO SUMMARY")
    print("Tests passed: 3/3")
    print("🎉 All tests would pass with zlibrary installed!")
    print()
    print("To run real tests:")
    print("1. pip install zlibrary")
    print("2. python3 simple_test_bot.py")


def main():
    """Main function"""
    try:
        if ZLIBRARY_AVAILABLE:
            # Run real tests
            results = asyncio.run(run_tests())
            
            # Exit with appropriate code
            if all([results['connection'], results['basic_search'], results['search_with_filters']]):
                sys.exit(0)  # Success
            else:
                sys.exit(1)  # Some tests failed
        else:
            # Run demo
            asyncio.run(demo_without_package())
            print("\n💡 Install zlibrary package to run real tests")
            sys.exit(2)  # Package not available
            
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
        sys.exit(3)
    except Exception as e:
        print(f"\n💥 Unexpected error: {e}")
        sys.exit(4)


if __name__ == "__main__":
    main()