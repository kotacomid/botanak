#!/usr/bin/env python3
"""
Minimal Z-Library Test
Quick verification of Z-Library functionality
"""

import asyncio

# Test the package availability
try:
    import zlibrary
    AVAILABLE = True
    print("✅ zlibrary package found")
except ImportError:
    AVAILABLE = False
    print("❌ zlibrary package not installed")
    print("Run: pip install zlibrary")


async def minimal_test():
    """Minimal test of Z-Library functionality"""
    if not AVAILABLE:
        print("💡 Cannot test without zlibrary package")
        return False
    
    try:
        print("🔗 Connecting to Z-Library...")
        lib = zlibrary.AsyncZlib()
        
        print("🔍 Searching for books...")
        paginator = await lib.search(q="python", count=1)
        results = await paginator.next()
        
        if results:
            book = results[0]
            print(f"✅ Found book: {book.get('name', 'Unknown')}")
            return True
        else:
            print("⚠️ No results found")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def main():
    """Main test function"""
    print("🧪 Minimal Z-Library Test")
    print("-" * 30)
    
    if AVAILABLE:
        success = asyncio.run(minimal_test())
        if success:
            print("🎉 Test passed!")
        else:
            print("⚠️ Test completed with issues")
    else:
        print("📦 Install zlibrary package first:")
        print("   pip install zlibrary")


if __name__ == "__main__":
    main()