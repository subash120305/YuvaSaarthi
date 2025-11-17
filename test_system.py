"""
Quick Test Script for YuvaSaarthi
Tests API connectivity and basic functionality
"""

import os
import sys
from pathlib import Path

# Add project to path
sys.path.insert(0, str(Path(__file__).parent))

def test_environment():
    """Test environment setup"""
    print("\n" + "="*60)
    print("YUVASAARTHI - SYSTEM TEST")
    print("="*60)

    # Check .env file
    env_file = Path(".env")
    if env_file.exists():
        print("\n[OK] .env file found")
    else:
        print("\n[ERROR] .env file not found")
        return False

    # Load environment
    from dotenv import load_dotenv
    load_dotenv()

    # Check Groq API key
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key and groq_key != "your_groq_api_key_here":
        print(f"[OK] Groq API key configured (starts with: {groq_key[:10]}...)")
    else:
        print("[ERROR] Groq API key not configured")
        return False

    return True


def test_groq_connection():
    """Test Groq API connectivity"""
    print("\n" + "-"*60)
    print("Testing Groq API Connection...")
    print("-"*60)

    try:
        from groq import Groq
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        # Simple test
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": "Say 'Hello from YuvaSaarthi!' in one sentence."}],
            max_tokens=50
        )

        answer = response.choices[0].message.content
        print(f"\n[OK] Groq API is working!")
        print(f"Test Response: {answer}")
        return True

    except Exception as e:
        print(f"\n[ERROR] Groq API test failed: {e}")
        return False


def test_documents():
    """Check if documents exist"""
    print("\n" + "-"*60)
    print("Checking Sample Documents...")
    print("-"*60)

    docs_dir = Path("data/documents")

    if not docs_dir.exists():
        print("\n[ERROR] Documents directory not found")
        print("Run: python create_sample_data.py")
        return False

    # Find PDFs
    pdfs = list(docs_dir.rglob("*.pdf"))

    if not pdfs:
        print("\n[ERROR] No PDF files found")
        print("Run: python create_sample_data.py")
        return False

    print(f"\n[OK] Found {len(pdfs)} PDF files:")
    for pdf in pdfs:
        rel_path = pdf.relative_to(docs_dir)
        print(f"  - {rel_path}")

    return True


def quick_chat_test():
    """Quick chat test"""
    print("\n" + "-"*60)
    print("Quick Chat Test...")
    print("-"*60)

    try:
        from groq import Groq
        client = Groq(api_key=os.getenv("GROQ_API_KEY"))

        # Test questions
        questions = [
            "What is 2+2?",
            "पाइथागोरस प्रमेय क्या है?",  # What is Pythagoras theorem?
        ]

        for i, question in enumerate(questions, 1):
            print(f"\n[Test {i}] Question: {question}")

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are a helpful educational assistant. Answer briefly."},
                    {"role": "user", "content": question}
                ],
                max_tokens=100,
                temperature=0.7
            )

            answer = response.choices[0].message.content
            print(f"Answer: {answer[:150]}...")

        print("\n[OK] Chat tests passed!")
        return True

    except Exception as e:
        print(f"\n[ERROR] Chat test failed: {e}")
        return False


def main():
    """Run all tests"""

    results = {
        "Environment": False,
        "Groq Connection": False,
        "Documents": False,
        "Chat Test": False
    }

    # Test environment
    results["Environment"] = test_environment()
    if not results["Environment"]:
        print("\n" + "="*60)
        print("SETUP REQUIRED")
        print("="*60)
        print("\n1. Make sure .env file exists")
        print("2. Add your Groq API key to .env")
        return

    # Test Groq
    results["Groq Connection"] = test_groq_connection()

    # Test documents
    results["Documents"] = test_documents()

    # Quick chat test
    if results["Groq Connection"]:
        results["Chat Test"] = quick_chat_test()

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    for test_name, passed in results.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} {test_name}")

    all_passed = all(results.values())

    if all_passed:
        print("\n" + "="*60)
        print("[SUCCESS] All tests passed!")
        print("="*60)
        print("\nNext steps:")
        print("1. Run: python ingest_documents.py")
        print("2. Then: streamlit run streamlit_app.py")
        print("   OR:   python telegram_bot.py")
    else:
        print("\n" + "="*60)
        print("[WARNING] Some tests failed")
        print("="*60)
        print("\nCheck the errors above and fix them.")

    print("\n")


if __name__ == "__main__":
    main()
