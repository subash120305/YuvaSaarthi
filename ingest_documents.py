"""
Robust Document Ingestion Script
Handles PDFs, Markdown files, and creates vector database with comprehensive error handling
"""

import sys
from pathlib import Path
from loguru import logger
import traceback

# Setup logging
logger.remove()
logger.add(sys.stderr, level="INFO")
logger.add("logs/ingestion.log", rotation="10 MB", level="DEBUG")

from backend.document_processor import DocumentProcessor
from utils.config import DOCUMENTS_DIR, VECTOR_DB_DIR


def count_files(directory: Path, extensions: list) -> dict:
    """Count files by extension"""
    counts = {ext: 0 for ext in extensions}
    for ext in extensions:
        counts[ext] = len(list(directory.rglob(f"*.{ext}")))
    return counts


def main():
    """Main ingestion function with robust error handling"""
    print("\n" + "=" * 70)
    print("🎓 YuvaSaarthi - Document Ingestion System")
    print("=" * 70 + "\n")

    try:
        # Ensure logs directory exists
        Path("logs").mkdir(exist_ok=True)

        # Check if documents directory exists
        if not DOCUMENTS_DIR.exists():
            print(f"📁 Creating documents directory: {DOCUMENTS_DIR}")
            DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
            
            # Create subdirectories
            for subdir in ["textbooks", "knowledge_base", "administrative", "admissions", "engineering", "polytechnic", "general"]:
                (DOCUMENTS_DIR / subdir).mkdir(exist_ok=True)
            
            print("✅ Directory structure created\n")
            print("⚠️  No documents found to ingest.\n")
            print("📝 Next steps:")
            print("   1. Add PDF files to: data/documents/textbooks/")
            print("   2. Add markdown files to: data/documents/knowledge_base/")
            print("   3. Run this script again\n")
            return 0

        # Count files
        file_counts = count_files(DOCUMENTS_DIR, ["pdf", "md", "txt"])
        total_files = sum(file_counts.values())

        if total_files == 0:
            print("⚠️  No supported files found in documents directory\n")
            print("📝 Supported file types: PDF (.pdf), Markdown (.md), Text (.txt)\n")
            print("📂 Please add files to:")
            print(f"   {DOCUMENTS_DIR.absolute()}\n")
            print("💡 Try running: python create_sample_data.py\n")
            return 0

        # Display file statistics
        print(f"📊 Found {total_files} file(s) to process:")
        for ext, count in file_counts.items():
            if count > 0:
                print(f"   • {count} {ext.upper()} file(s)")
        print()

        # List first 15 files
        all_files = []
        for ext in ["pdf", "md", "txt"]:
            all_files.extend(DOCUMENTS_DIR.rglob(f"*.{ext}"))
        
        print("📄 Files to be processed:")
        for i, file_path in enumerate(sorted(all_files)[:15], 1):
            rel_path = file_path.relative_to(DOCUMENTS_DIR)
            size_kb = file_path.stat().st_size / 1024
            print(f"   {i:2d}. {rel_path} ({size_kb:.1f} KB)")
        
        if len(all_files) > 15:
            print(f"   ... and {len(all_files) - 15} more file(s)")
        print()

        # Check for vector store
        vector_store_exists = VECTOR_DB_DIR.exists()
        if vector_store_exists:
            print(f"⚠️  Existing vector store found at: {VECTOR_DB_DIR}")
            print("   Recreating will delete the existing database.\n")

        print("-" * 70)
        
        # Ask for confirmation
        response = input("\n▶️  Proceed with ingestion? (yes/no): ").strip().lower()
        if response not in ['yes', 'y']:
            print("\n❌ Ingestion cancelled by user\n")
            return 0

        force_refresh = False
        if vector_store_exists:
            response = input("▶️  Recreate vector store from scratch? (yes/no): ").strip().lower()
            force_refresh = response in ['yes', 'y']

        print("\n" + "=" * 70)
        print("🚀 Starting document ingestion...")
        print("=" * 70 + "\n")

        # Initialize processor
        print("🔧 Initializing document processor...")
        processor = DocumentProcessor()
        print("✅ Document processor ready\n")

        # Ingest documents
        print("📚 Processing and embedding documents...")
        print("   (This may take a few minutes for large document sets)\n")
        
        vector_store = processor.ingest_documents(force_refresh=force_refresh)

        if vector_store:
            print("\n" + "=" * 70)
            print("✅ DOCUMENT INGESTION COMPLETED SUCCESSFULLY!")
            print("=" * 70)
            
            print(f"\n📊 Ingestion Statistics:")
            print(f"   • Total files processed: {total_files}")
            print(f"   • Vector store location: {VECTOR_DB_DIR}")
            print(f"   • Status: ✅ Ready for use")

            print("\n🚀 Next Steps:")
            print("   Run one of the following commands:\n")
            print("   1️⃣  Web Interface:")
            print("       streamlit run streamlit_app.py\n")
            print("   2️⃣  Telegram Bot:")
            print("       python telegram_bot.py\n")
            print("   3️⃣  Test the system:")
            print("       python -m backend.chatbot_engine\n")

        else:
            print("\n" + "=" * 70)
            print("❌ DOCUMENT INGESTION FAILED")
            print("=" * 70)
            print("\n⚠️  No documents were successfully processed")
            print("\n🔍 Troubleshooting steps:")
            print("   1. Check that PDF files are not corrupted")
            print("   2. Ensure PDFs contain selectable text (not scanned images)")
            print("   3. Verify you have sufficient disk space")
            print("   4. Check logs/ingestion.log for detailed error messages\n")
            return 1

    except KeyboardInterrupt:
        print("\n\n⚠️  Ingestion interrupted by user (Ctrl+C)")
        print("   You may need to run the script again to complete ingestion\n")
        return 1

    except Exception as e:
        logger.error(f"Fatal error during ingestion: {e}")
        logger.error(traceback.format_exc())
        
        print("\n" + "=" * 70)
        print("❌ FATAL ERROR OCCURRED")
        print("=" * 70)
        print(f"\n💥 Error: {str(e)}\n")
        print("🔍 Troubleshooting:")
        print("   1. Check logs/ingestion.log for detailed error trace")
        print("   2. Ensure all dependencies are installed:")
        print("      pip install -r requirements.txt")
        print("   3. Verify Python version is 3.9 or higher")
        print("   4. Check that you have write permissions to data/ directory\n")
        print("📧 If the error persists, please report it with the log file.\n")
        return 1

    print()
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
