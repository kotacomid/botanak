#!/usr/bin/env python3
"""
Simple Test Script for Book Scraping Bot
Tests basic functionality without complex dependencies
"""

import os
import sys
from pathlib import Path

def test_basic_imports():
    """Test basic Python imports"""
    print("🧪 Testing basic imports...")
    
    try:
        import json
        print("✅ json imported")
        
        import csv
        print("✅ csv imported")
        
        import re
        print("✅ re imported")
        
        import requests
        print("✅ requests imported")
        
        return True
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return False

def test_configuration():
    """Test simple configuration"""
    print("\n⚙️ Testing configuration...")
    
    try:
        # Simple configuration test
        app_name = "Book Scraping Bot"
        version = "1.0.0"
        debug = os.getenv("DEBUG", "false").lower() in ('true', '1', 'yes')
        
        print(f"App: {app_name}")
        print(f"Version: {version}")
        print(f"Debug: {debug}")
        print("✅ Configuration loaded")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_directories():
    """Test directory creation"""
    print("\n📁 Testing directories...")
    
    try:
        # Create basic directories
        directories = [
            "output",
            "output/metadata",
            "output/books", 
            "output/covers",
            "output/html"
        ]
        
        for directory in directories:
            Path(directory).mkdir(parents=True, exist_ok=True)
            print(f"✅ {directory} created/verified")
        
        return True
    except Exception as e:
        print(f"❌ Directory test failed: {e}")
        return False

def test_simple_scraper():
    """Test simple scraping functionality"""
    print("\n🔍 Testing simple scraper...")
    
    try:
        import requests
        
        # Test basic HTTP functionality
        print("✅ HTTP client available")
        
        # Test URL building
        base_url = "https://annas-archive.org"
        search_url = f"{base_url}/search"
        print(f"✅ URL building works: {search_url}")
        
        return True
    except Exception as e:
        print(f"❌ Scraper test failed: {e}")
        return False

def test_simple_metadata():
    """Test simple metadata handling"""
    print("\n📝 Testing metadata handling...")
    
    try:
        # Simple metadata structure
        metadata = {
            "title": "Test Book",
            "author": "Test Author",
            "year": 2023,
            "format": "PDF"
        }
        
        # Test JSON serialization
        import json
        json_str = json.dumps(metadata, indent=2)
        print("✅ JSON serialization works")
        
        # Test filename creation
        import re
        def simple_slugify(text):
            if not text:
                return ""
            # Simple slugify
            text = re.sub(r'[^\w\s-]', '', text.lower())
            text = re.sub(r'[-\s]+', '-', text)
            return text.strip('-')
        
        filename = simple_slugify(metadata["title"])
        print(f"✅ Filename generation works: {filename}")
        
        return True
    except Exception as e:
        print(f"❌ Metadata test failed: {e}")
        return False

def test_file_operations():
    """Test basic file operations"""
    print("\n💾 Testing file operations...")
    
    try:
        # Test file writing
        test_file = Path("output/test.txt")
        test_file.write_text("Test content", encoding='utf-8')
        print("✅ File writing works")
        
        # Test file reading
        content = test_file.read_text(encoding='utf-8')
        print("✅ File reading works")
        
        # Cleanup
        test_file.unlink(missing_ok=True)
        print("✅ File cleanup works")
        
        return True
    except Exception as e:
        print(f"❌ File operations test failed: {e}")
        return False

def simple_demo():
    """Run a simple demo"""
    print("\n🚀 Simple Demo...")
    
    try:
        # Create sample book data
        sample_book = {
            "title": "Learn Python Programming",
            "author": "John Doe",
            "year": 2023,
            "format": "PDF",
            "size": "15.2 MB",
            "source": "demo"
        }
        
        print("📚 Sample Book Data:")
        for key, value in sample_book.items():
            print(f"   {key}: {value}")
        
        # Save to JSON
        import json
        output_dir = Path("output/metadata")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        json_file = output_dir / "sample_book.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(sample_book, f, indent=2)
        
        print(f"✅ Sample data saved to: {json_file}")
        
        return True
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        return False

def main():
    """Run all simple tests"""
    print("🚀 Book Scraping Bot - Simple Test Suite")
    print("=" * 50)
    
    tests = [
        ("Basic Imports", test_basic_imports),
        ("Configuration", test_configuration),
        ("Directories", test_directories),
        ("Simple Scraper", test_simple_scraper),
        ("Metadata Handling", test_simple_metadata),
        ("File Operations", test_file_operations),
        ("Simple Demo", simple_demo)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*15} {test_name} {'='*15}")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} CRASHED: {e}")
    
    print(f"\n{'='*50}")
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All basic tests passed!")
        print("\n🚀 You can now try:")
        print("1. Install missing dependencies:")
        print("   pip install requests beautifulsoup4")
        print("2. Try a simple search:")
        print("   python -c \"import requests; print('Requests working!')\"")
        print("3. Check the output/ folder for generated files")
    else:
        print("⚠️ Some basic tests failed.")
        print("💡 Try installing basic dependencies first:")
        print("   pip install requests beautifulsoup4 lxml")

if __name__ == "__main__":
    main()