#!/usr/bin/env python3
"""
Setup script for Book Scraping Bot
"""

import os
import sys
import subprocess
from pathlib import Path

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def setup_environment():
    """Setup environment configuration"""
    print("⚙️ Setting up environment...")
    
    env_example = Path(".env.example")
    env_file = Path(".env")
    
    if env_example.exists() and not env_file.exists():
        import shutil
        shutil.copy(env_example, env_file)
        print("✅ Created .env file from template")
        print("📝 Please edit .env file with your configuration")
        return True
    elif env_file.exists():
        print("ℹ️ .env file already exists")
        return True
    else:
        print("❌ .env.example not found")
        return False

def create_directories():
    """Create necessary directories"""
    print("📁 Creating directories...")
    
    directories = [
        "output",
        "output/metadata",
        "output/books", 
        "output/covers",
        "output/html",
        "config",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Directories created")
    return True

def test_installation():
    """Test if installation works"""
    print("🧪 Testing installation...")
    
    try:
        # Test imports
        from config.settings import settings
        from core.metadata import BookMetadata
        print("✅ Core modules imported successfully")
        
        # Test configuration
        if settings.APP_NAME:
            print(f"✅ Configuration loaded: {settings.APP_NAME} v{settings.VERSION}")
        
        return True
    except Exception as e:
        print(f"❌ Installation test failed: {e}")
        return False

def show_next_steps():
    """Show what user should do next"""
    print("\n🎉 Setup completed!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your API keys and settings")
    print("2. Run: python main.py search \"test query\" --limit 3")
    print("3. Check the output/ directory for results")
    print("4. Read USAGE.md for detailed instructions")
    print("\n🚀 Quick start:")
    print("   python main.py search \"python programming\" --limit 5")
    print("   python run_example.py")

def main():
    """Main setup function"""
    print("🚀 Book Scraping Bot Setup")
    print("=" * 40)
    
    steps = [
        ("Installing dependencies", install_dependencies),
        ("Setting up environment", setup_environment),
        ("Creating directories", create_directories),
        ("Testing installation", test_installation)
    ]
    
    success = True
    
    for step_name, step_func in steps:
        print(f"\n{step_name}...")
        if not step_func():
            success = False
            break
    
    if success:
        show_next_steps()
    else:
        print("\n❌ Setup failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()