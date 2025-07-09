#!/usr/bin/env python3
"""
Install and Test Z-Library Bot
Automatically installs zlibrary package and runs tests
"""

import subprocess
import sys
import asyncio
from pathlib import Path


def install_zlibrary():
    """Install zlibrary package"""
    print("📦 Installing zlibrary package...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "zlibrary"])
        print("✅ zlibrary package installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install zlibrary: {e}")
        return False


def check_zlibrary():
    """Check if zlibrary is available"""
    try:
        import zlibrary
        print("✅ zlibrary package is available")
        return True
    except ImportError:
        print("❌ zlibrary package not found")
        return False


async def quick_test():
    """Run a quick test of Z-Library functionality"""
    print("\n🧪 Running quick Z-Library test...")
    
    try:
        import zlibrary
        
        # Initialize Z-Library
        lib = zlibrary.AsyncZlib()
        print("✅ Z-Library initialized")
        
        # Test basic search
        print("🔍 Testing search for 'programming'...")
        paginator = await lib.search(q="programming", count=2)
        results = await paginator.next()
        
        print(f"✅ Search successful - found {len(results)} results")
        
        if results:
            first_book = results[0]
            print(f"📚 Sample result: {first_book.get('name', 'Unknown')}")
            
            # Save sample result
            output_dir = Path("test_output")
            output_dir.mkdir(exist_ok=True)
            
            import json
            with open(output_dir / "sample_result.json", 'w') as f:
                json.dump(first_book, f, indent=2)
            print(f"💾 Sample result saved to test_output/sample_result.json")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def main():
    """Main function"""
    print("🚀 Z-Library Package Installer and Tester")
    print("=" * 50)
    
    # Check if already installed
    if not check_zlibrary():
        print("\n📥 zlibrary package not found. Installing...")
        
        # Ask user for permission
        try:
            response = input("Install zlibrary package? (y/n): ").lower().strip()
            if response not in ['y', 'yes']:
                print("Installation cancelled.")
                return
        except KeyboardInterrupt:
            print("\nInstallation cancelled.")
            return
        
        # Install package
        if not install_zlibrary():
            print("❌ Installation failed. Exiting.")
            return
    
    # Run test
    print("\n🧪 Running functionality test...")
    try:
        success = asyncio.run(quick_test())
        
        if success:
            print("\n🎉 Test completed successfully!")
            print("✅ Z-Library bot is ready to use")
            print("\nNext steps:")
            print("- Run: python3 simple_test_bot.py")
            print("- Or: python3 zlibrary_example.py")
        else:
            print("\n⚠️ Test completed with issues")
            print("The package is installed but there might be connectivity issues")
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")


if __name__ == "__main__":
    main()