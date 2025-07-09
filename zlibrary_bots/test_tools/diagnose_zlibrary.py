#!/usr/bin/env python3
"""
Z-Library Diagnostic Tool
Helps troubleshoot zlibrary package installation and import issues
"""

import sys
import subprocess
import importlib.util

def check_python_version():
    """Check Python version"""
    print(f"🐍 Python version: {sys.version}")
    print(f"📍 Python executable: {sys.executable}")
    
def check_pip_list():
    """Check if zlibrary is in pip list"""
    print("\n📦 Checking installed packages...")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "list"], 
                              capture_output=True, text=True)
        pip_output = result.stdout
        
        if "zlibrary" in pip_output.lower():
            for line in pip_output.split('\n'):
                if "zlibrary" in line.lower():
                    print(f"✅ Found in pip list: {line}")
                    return True
        else:
            print("❌ zlibrary not found in pip list")
            return False
    except Exception as e:
        print(f"❌ Error checking pip list: {e}")
        return False

def test_direct_import():
    """Test direct import of zlibrary"""
    print("\n🧪 Testing direct import...")
    try:
        import zlibrary
        print("✅ Direct import successful")
        print(f"📍 zlibrary location: {zlibrary.__file__}")
        print(f"📊 zlibrary version: {getattr(zlibrary, '__version__', 'Unknown')}")
        return True
    except ImportError as e:
        print(f"❌ Direct import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during import: {e}")
        return False

def test_submodule_imports():
    """Test importing specific components"""
    print("\n🔧 Testing submodule imports...")
    try:
        from zlibrary import Language, Extension
        print("✅ Language and Extension imports successful")
        print(f"📋 Available languages: {list(Language)[:5]}... (showing first 5)")
        print(f"📄 Available extensions: {list(Extension)[:5]}... (showing first 5)")
        return True
    except ImportError as e:
        print(f"❌ Submodule import failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error during submodule import: {e}")
        return False

def test_async_class():
    """Test AsyncZlib class"""
    print("\n⚡ Testing AsyncZlib class...")
    try:
        import zlibrary
        lib = zlibrary.AsyncZlib()
        print("✅ AsyncZlib class created successfully")
        return True
    except Exception as e:
        print(f"❌ AsyncZlib creation failed: {e}")
        return False

def suggest_solutions(import_success, pip_success):
    """Suggest solutions based on test results"""
    print("\n🔧 SUGGESTED SOLUTIONS")
    print("=" * 40)
    
    if not pip_success:
        print("1. 📦 Reinstall zlibrary package:")
        print("   pip uninstall zlibrary -y")
        print("   pip install zlibrary")
        print()
        
    if pip_success and not import_success:
        print("2. 🔄 Try different installation methods:")
        print("   pip install --force-reinstall zlibrary")
        print("   # OR")
        print("   pip install --upgrade zlibrary")
        print()
        
    print("3. 🧹 Clear Python cache:")
    print("   python -c \"import sys; print(sys.path)\"")
    print("   # Remove any __pycache__ directories")
    print()
    
    print("4. 🐍 Check Python environment:")
    print("   which python")
    print("   which pip")
    print("   # Make sure you're using the same Python for both")
    print()
    
    print("5. 🔍 Manual verification:")
    print("   python -c \"import zlibrary; print('Success')\"")

def create_simple_test():
    """Create a simple test file that should work"""
    print("\n📝 Creating simple test file...")
    
    simple_test_content = '''#!/usr/bin/env python3
"""
Simple Z-Library Test - Fixed Version
This version has better error handling for import issues
"""

import sys

def test_zlibrary():
    """Test zlibrary with detailed error reporting"""
    print("🧪 Testing zlibrary import...")
    
    try:
        print("Step 1: Importing zlibrary...")
        import zlibrary
        print("✅ zlibrary imported successfully")
        
        print("Step 2: Importing components...")
        from zlibrary import Language, Extension
        print("✅ Components imported successfully")
        
        print("Step 3: Creating AsyncZlib instance...")
        lib = zlibrary.AsyncZlib()
        print("✅ AsyncZlib created successfully")
        
        print("🎉 All tests passed! zlibrary is working correctly.")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Try: pip install --force-reinstall zlibrary")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Simple Z-Library Test")
    print("=" * 30)
    
    if test_zlibrary():
        print("\\n✅ Ready to use Z-Library!")
        print("You can now run the main examples.")
    else:
        print("\\n❌ Z-Library is not working properly.")
        print("Please follow the installation suggestions.")
'''

    try:
        with open('simple_zlibrary_test.py', 'w', encoding='utf-8') as f:
            f.write(simple_test_content)
        print("✅ Created 'simple_zlibrary_test.py'")
        print("   Run it with: python simple_zlibrary_test.py")
    except Exception as e:
        print(f"❌ Failed to create test file: {e}")

def main():
    """Main diagnostic function"""
    print("🔧 Z-Library Installation Diagnostic")
    print("=" * 50)
    
    # Run diagnostics
    check_python_version()
    pip_success = check_pip_list()
    import_success = test_direct_import()
    
    if import_success:
        submodule_success = test_submodule_imports()
        if submodule_success:
            async_success = test_async_class()
            if async_success:
                print("\n🎉 ALL TESTS PASSED!")
                print("✅ zlibrary is working correctly")
                print("You can now run the Z-Library examples!")
                return
    
    # If we get here, there are issues
    print("\n⚠️ ISSUES DETECTED")
    suggest_solutions(import_success, pip_success)
    create_simple_test()
    
    print("\n🔗 Next Steps:")
    print("1. Follow the suggested solutions above")
    print("2. Run: python simple_zlibrary_test.py")
    print("3. If still having issues, try a fresh Python environment")

if __name__ == "__main__":
    main()