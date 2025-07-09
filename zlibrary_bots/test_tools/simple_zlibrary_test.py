#!/usr/bin/env python3
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
        print("\n✅ Ready to use Z-Library!")
        print("You can now run the main examples.")
    else:
        print("\n❌ Z-Library is not working properly.")
        print("Please follow the installation suggestions.")
