"""
Test script to verify jack module imports work correctly
"""
import sys
import os

# Add server directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing jack module imports...")
    
    # Test Compiler imports
    print("1. Testing Compiler imports...")
    from jack.Compiler.JackAnalyzer import JackAnalyzer
    print("   ✓ JackAnalyzer imported successfully")
    
    # Test VMTranslator imports
    print("2. Testing VMTranslator imports...")
    from jack.VMTranslator.main import VMTranslator
    print("   ✓ VMTranslator imported successfully")
    
    # Test Assembler imports
    print("3. Testing Assembler imports...")
    from jack.Assembler.main import assemble_file
    print("   ✓ assemble_file imported successfully")
    
    # Test main module
    print("4. Testing main module...")
    from jack.main import compile_jack_to_hack
    print("   ✓ compile_jack_to_hack imported successfully")
    
    print("\n✅ All imports successful!")
    
except Exception as e:
    print(f"\n❌ Import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
