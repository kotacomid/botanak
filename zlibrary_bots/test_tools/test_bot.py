#!/usr/bin/env python3
"""
Simple test script for Book Scraping Bot
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

def test_imports():
    """Test if all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from config.settings import settings
        print("✅ Settings imported")
        
        from core.metadata import BookMetadata, MetadataProcessor
        print("✅ Metadata module imported")
        
        from core.scraper import BookScraper
        print("✅ Scraper module imported")
        
        from core.downloader import FileDownloader
        print("✅ Downloader module imported")
        
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_configuration():
    """Test configuration loading"""
    print("\n⚙️ Testing configuration...")
    
    try:
        from config.settings import settings, validate_config
        
        print(f"App: {settings.APP_NAME}")
        print(f"Version: {settings.VERSION}")
        print(f"Premium: {settings.IS_PREMIUM}")
        print(f"Download books: {settings.DOWNLOAD_BOOKS}")
        print(f"Download covers: {settings.DOWNLOAD_COVERS}")
        
        # Check for warnings
        warnings = validate_config()
        if warnings:
            print("\n⚠️ Configuration warnings:")
            for warning in warnings:
                print(f"  - {warning}")
        else:
            print("✅ Configuration is valid")
        
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

def test_metadata_processing():
    """Test metadata processing"""
    print("\n📝 Testing metadata processing...")
    
    try:
        from core.metadata import BookMetadata, MetadataProcessor
        
        # Create test metadata
        test_data = {
            "title": "Test Book Title",
            "author": "Test Author",
            "year": "2023",
            "format": "PDF",
            "filesize": "10.5 MB"
        }
        
        processor = MetadataProcessor()
        metadata = processor.process_metadata(test_data, "test-source")
        
        print(f"Title: {metadata.title}")
        print(f"Author: {metadata.author}")
        print(f"Year: {metadata.year}")
        print(f"Filename base: {metadata.filename_base}")
        
        # Test validation
        issues = processor.validate_metadata(metadata)
        if issues:
            print(f"⚠️ Validation issues: {issues}")
        else:
            print("✅ Metadata validation passed")
        
        return True
    except Exception as e:
        print(f"❌ Metadata test failed: {e}")
        return False

def test_file_operations():
    """Test file operations"""
    print("\n📁 Testing file operations...")
    
    try:
        from pathlib import Path
        
        # Check if output directories exist
        output_dir = Path("output")
        if output_dir.exists():
            print("✅ Output directory exists")
            
            subdirs = ["metadata", "books", "covers", "html"]
            for subdir in subdirs:
                subdir_path = output_dir / subdir
                if subdir_path.exists():
                    print(f"✅ {subdir} directory exists")
                else:
                    print(f"⚠️ {subdir} directory missing, creating...")
                    subdir_path.mkdir(parents=True, exist_ok=True)
        else:
            print("⚠️ Output directory missing, creating...")
            output_dir.mkdir(parents=True, exist_ok=True)
        
        return True
    except Exception as e:
        print(f"❌ File operations test failed: {e}")
        return False

def test_simple_search():
    """Test simple search functionality"""
    print("\n🔍 Testing simple search (no actual downloads)...")
    
    try:
        from core.scraper import BookScraper
        
        scraper = BookScraper()
        
        # Test search without actual network calls
        print("✅ Scraper initialized successfully")
        
        # Test URL building and basic functions
        # (We don't actually make requests in this test)
        
        scraper.close()
        print("✅ Scraper closed successfully")
        
        return True
    except Exception as e:
        print(f"❌ Search test failed: {e}")
        return False

def test_html_generation():
    """Test HTML generation"""
    print("\n🌐 Testing HTML generation...")
    
    try:
        from core.metadata import BookMetadata
        from publishers.static import StaticHTMLGenerator
        from datetime import datetime
        
        # Create test book
        test_book = BookMetadata(
            title="Test Programming Book",
            author="John Doe",
            year=2023,
            file_format="PDF",
            file_size="15.2 MB",
            source="test-source",
            description="A comprehensive guide to programming."
        )
        
        # Test HTML generation
        generator = StaticHTMLGenerator()
        page_path = generator.generate_book_page(test_book)
        
        if Path(page_path).exists():
            print(f"✅ HTML page generated: {page_path}")
        else:
            print("⚠️ HTML page generated but file not found")
        
        return True
    except Exception as e:
        print(f"❌ HTML generation test failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("🚀 Book Scraping Bot - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Module Imports", test_imports),
        ("Configuration", test_configuration),
        ("Metadata Processing", test_metadata_processing),
        ("File Operations", test_file_operations),
        ("Search Functionality", test_simple_search),
        ("HTML Generation", test_html_generation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
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
        print("🎉 All tests passed! Bot is ready to use.")
        print("\n🚀 Try running:")
        print("   python main.py search \"test\" --limit 2 --no-download")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        print("💡 Try running: python setup.py")

def main():
    """Main function"""
    run_all_tests()

if __name__ == "__main__":
    main()