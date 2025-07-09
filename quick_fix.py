#!/usr/bin/env python3
"""
Quick Fix Script for Book Scraping Bot
Resolves common installation and dependency issues
"""

import os
import sys
import subprocess
from pathlib import Path

def fix_dependencies():
    """Install minimal dependencies"""
    print("🔧 Installing minimal dependencies...")
    
    minimal_packages = [
        "requests",
        "beautifulsoup4", 
        "lxml"
    ]
    
    for package in minimal_packages:
        try:
            print(f"📦 Installing {package}...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", package, "--user"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f"✅ {package} installed")
        except subprocess.CalledProcessError:
            print(f"⚠️ Could not install {package} (may already be installed)")

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "output",
        "output/metadata",
        "output/books", 
        "output/covers",
        "output/html",
        "config"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ {directory}")

def create_simple_env():
    """Create simple .env file if it doesn't exist"""
    print("\n⚙️ Creating .env file...")
    
    env_file = Path(".env")
    if not env_file.exists():
        env_content = """# Book Scraping Bot Configuration
DEBUG=false
IS_PREMIUM=false
OUTPUT_DIR=output
DOWNLOAD_BOOKS=true
DOWNLOAD_COVERS=true
MAX_FILE_SIZE_MB=100
SCRAPING_DELAY=1.0
REQUESTS_PER_MINUTE=60
"""
        env_file.write_text(env_content)
        print("✅ .env file created")
    else:
        print("✅ .env file already exists")

def create_simple_demo():
    """Create a simple working demo"""
    print("\n🚀 Creating simple demo...")
    
    demo_content = '''#!/usr/bin/env python3
"""
Simple Book Scraping Demo
Works without complex dependencies
"""

import json
import re
from pathlib import Path

def slugify(text, max_length=50):
    """Simple slugify function"""
    if not text:
        return ""
    text = re.sub(r'[^\\w\\s-]', '', text.lower())
    text = re.sub(r'[-\\s]+', '-', text)
    return text.strip('-')[:max_length]

def create_sample_book():
    """Create sample book data"""
    book = {
        "title": "Python Programming Guide",
        "author": "Demo Author", 
        "year": 2023,
        "format": "PDF",
        "size": "12.5 MB",
        "source": "demo",
        "description": "A comprehensive guide to Python programming.",
        "filename_base": slugify("Python Programming Guide Demo Author")
    }
    return book

def save_metadata(book):
    """Save book metadata"""
    output_dir = Path("output/metadata")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Save JSON
    json_file = output_dir / f"{book['filename_base']}.json"
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(book, f, indent=2)
    
    print(f"✅ Metadata saved: {json_file}")
    return str(json_file)

def create_simple_html(book):
    """Create simple HTML page"""
    html_dir = Path("output/html")
    html_dir.mkdir(parents=True, exist_ok=True)
    
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>{book['title']} by {book['author']}</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        .book {{ max-width: 600px; margin: 0 auto; }}
        h1 {{ color: #333; }}
        .meta {{ background: #f5f5f5; padding: 20px; margin: 20px 0; }}
    </style>
</head>
<body>
    <div class="book">
        <h1>{book['title']}</h1>
        <h2>by {book['author']}</h2>
        
        <div class="meta">
            <strong>Year:</strong> {book['year']}<br>
            <strong>Format:</strong> {book['format']}<br>
            <strong>Size:</strong> {book['size']}<br>
            <strong>Source:</strong> {book['source']}
        </div>
        
        <p>{book['description']}</p>
    </div>
</body>
</html>"""
    
    html_file = html_dir / f"{book['filename_base']}.html"
    html_file.write_text(html_content, encoding='utf-8')
    
    print(f"✅ HTML page created: {html_file}")
    return str(html_file)

def main():
    print("🚀 Simple Book Scraping Demo")
    print("=" * 40)
    
    # Create sample book
    book = create_sample_book()
    print(f"📚 Sample book: {book['title']}")
    
    # Save metadata
    json_file = save_metadata(book)
    
    # Create HTML
    html_file = create_simple_html(book)
    
    print("\\n✅ Demo completed successfully!")
    print("\\n📂 Check these files:")
    print(f"   📝 {json_file}")
    print(f"   🌐 {html_file}")

if __name__ == "__main__":
    main()
'''
    
    demo_file = Path("simple_demo.py")
    demo_file.write_text(demo_content)
    print(f"✅ Demo script created: {demo_file}")

def test_basic_functionality():
    """Test if basic functionality works"""
    print("\n🧪 Testing basic functionality...")
    
    try:
        import requests
        print("✅ Requests available")
    except ImportError:
        print("❌ Requests not available")
        return False
    
    try:
        import json
        test_data = {"test": "data"}
        json.dumps(test_data)
        print("✅ JSON processing works")
    except Exception:
        print("❌ JSON processing failed")
        return False
    
    return True

def main():
    """Main fix function"""
    print("🔧 Book Scraping Bot - Quick Fix")
    print("=" * 40)
    
    steps = [
        ("Installing dependencies", fix_dependencies),
        ("Creating directories", create_directories), 
        ("Creating .env file", create_simple_env),
        ("Creating demo", create_simple_demo),
        ("Testing functionality", test_basic_functionality)
    ]
    
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        try:
            success = step_func()
            if success is False:
                print(f"⚠️ {step_name} had issues")
            else:
                print(f"✅ {step_name} completed")
        except Exception as e:
            print(f"❌ {step_name} failed: {e}")
    
    print("\n🎉 Quick fix completed!")
    print("\n🚀 Try these commands:")
    print("1. python simple_test.py      # Run basic tests")  
    print("2. python simple_demo.py      # Run working demo")
    print("3. Check output/ folder for generated files")

if __name__ == "__main__":
    main()