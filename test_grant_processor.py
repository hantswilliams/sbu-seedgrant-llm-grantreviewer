#!/usr/bin/env python3
"""
Test script for the Grant Review Processor
"""

import sys
import os
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.append(str(project_root))

def test_basic_functionality():
    """Test basic functionality without requiring API keys"""
    print("Testing Grant Review Processor...")
    
    # Test 1: Basic imports
    try:
        from shared.db_adapter import get_db_adapter
        print("✅ Database adapter import successful")
    except Exception as e:
        print(f"❌ Database adapter import failed: {e}")
        return False
    
    # Test 2: Database initialization
    try:
        db_adapter = get_db_adapter()
        db_adapter.init_db()
        print("✅ Database initialization successful")
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        return False
    
    # Test 3: Check grant applications structure
    try:
        scenarios_dir = project_root / "llm" / "scenarios"
        if scenarios_dir.exists():
            applicants = [d for d in scenarios_dir.iterdir() if d.is_dir()]
            print(f"✅ Found {len(applicants)} grant applicants: {[a.name for a in applicants]}")
            
            # Check each applicant has required files
            required_files = ["biosketches.md", "budget.md", "coverpage.md", "project.md"]
            for applicant_dir in applicants:
                missing_files = []
                for req_file in required_files:
                    if not (applicant_dir / req_file).exists():
                        missing_files.append(req_file)
                
                if missing_files:
                    print(f"⚠️  {applicant_dir.name} missing: {missing_files}")
                else:
                    print(f"✅ {applicant_dir.name} has all required components")
        else:
            print("❌ Scenarios directory not found")
            return False
    except Exception as e:
        print(f"❌ Grant applications check failed: {e}")
        return False
    
    # Test 4: Check review instructions
    try:
        instructions_path = project_root / "llm" / "prompts" / "LLM_Grant_Review_Instructions.md"
        if instructions_path.exists():
            with open(instructions_path, 'r') as f:
                instructions = f.read()
                print(f"✅ Grant review instructions loaded ({len(instructions)} characters)")
        else:
            print("❌ Grant review instructions not found")
            return False
    except Exception as e:
        print(f"❌ Review instructions check failed: {e}")
        return False
    
    # Test 5: Test database operations
    try:
        conn = db_adapter.get_connection()
        
        # Test inserting a sample grant review
        if hasattr(db_adapter, 'insert_grant_review'):
            grant_review_id = db_adapter.insert_grant_review(
                conn,
                "TestApplicant",
                "TestVendor", 
                "TestModel",
                "v1.0",
                1,
                "2024-01-01T00:00:00",
                "Test prompt",
                "Test response",
                '[]',
                "Fund",
                1.5
            )
            print(f"✅ Grant review database insert successful (ID: {grant_review_id})")
            
            # Test inserting criterion
            if hasattr(db_adapter, 'insert_grant_review_criterion'):
                criterion_id = db_adapter.insert_grant_review_criterion(
                    conn,
                    grant_review_id,
                    "Innovation and Impact",
                    25,
                    "Test rationale"
                )
                print(f"✅ Grant review criterion insert successful (ID: {criterion_id})")
        
        db_adapter.close_connection(conn)
        print("✅ Database operations test successful")
    except Exception as e:
        print(f"❌ Database operations test failed: {e}")
        return False
    
    print("\n🎉 All basic tests passed! The grant review system is ready for testing.")
    return True

def test_processor_initialization():
    """Test processor initialization without API keys"""
    print("\nTesting processor initialization...")
    
    try:
        # Import the processor (but don't initialize API clients)
        from scripts.grant_review_processor import GrantReviewProcessor
        
        # Test with dummy API keys to avoid import errors
        os.environ["OPENAI_API_KEY"] = "dummy"
        os.environ["GEMINI_API_KEY"] = "dummy" 
        os.environ["CLAUDE_API_KEY"] = "dummy"
        os.environ["GROK_API_KEY"] = "dummy"
        
        # Create processor instance
        processor = GrantReviewProcessor()
        
        print(f"✅ Processor initialized successfully")
        print(f"✅ Found {len(processor.grant_applications)} grant applications")
        print(f"✅ Review instructions loaded: {len(processor.review_instructions)} characters")
        print(f"✅ Outputs directory created: {processor.outputs_dir}")
        
        # Test grant content loading
        if processor.grant_applications:
            sample_app = processor.grant_applications[0]
            content = processor._load_grant_components(sample_app)
            print(f"✅ Sample grant content loaded: {len(content)} characters")
            
            # Test prompt building
            full_prompt = processor._build_full_prompt(content)
            print(f"✅ Full prompt built: {len(full_prompt)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Processor initialization failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("Grant Review Processor Test Suite")
    print("=" * 60)
    
    test1_passed = test_basic_functionality()
    
    if test1_passed:
        test2_passed = test_processor_initialization()
        
        if test2_passed:
            print("\n" + "=" * 60)
            print("✅ ALL TESTS PASSED!")
            print("The grant review system is ready for use.")
            print("\nNext steps:")
            print("1. Set up API keys in .env file")
            print("2. Run: python scripts/grant_review_processor.py --model openai --applicant Daniel")
            print("=" * 60)
        else:
            print("\n❌ Some tests failed. Please check the issues above.")
    else:
        print("\n❌ Basic tests failed. Please check the setup.")