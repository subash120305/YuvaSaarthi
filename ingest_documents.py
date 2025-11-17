"""
Document Ingestion Script
Processes all PDFs and creates vector database
"""

import sys
from pathlib import Path
from loguru import logger

from backend.document_processor import DocumentProcessor
from utils.config import DOCUMENTS_DIR, VECTOR_DB_DIR


def main():
    """Main ingestion function"""
    print("\n" + "=" * 60)
    print("🎓 YuvaSaarthi - Document Ingestion")
    print("=" * 60 + "\n")

    # Check if documents directory exists
    if not DOCUMENTS_DIR.exists():
        print(f"❌ Documents directory not found: {DOCUMENTS_DIR}")
        print("\nCreating directory structure...")
        DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
        print("✓ Directory created")
        print("\n⚠️  No documents found to ingest.")
        print("\nNext steps:")
        print("1. Run: python create_sample_data.py (to create sample documents)")
        print("2. OR add your own PDFs to data/documents/textbooks/")
        print("3. Then run this script again")
        return

    # Count PDF files
    pdf_files = list(DOCUMENTS_DIR.rglob("*.pdf"))
    if not pdf_files:
        print("⚠️  No PDF files found in documents directory")
        print("\nNext steps:")
        print("1. Run: python create_sample_data.py (to create sample documents)")
        print("2. OR add your own PDFs to data/documents/")
        print("3. Then run this script again")
        return

    print(f"Found {len(pdf_files)} PDF files")
    print("\nPDF files to process:")
    for pdf_file in pdf_files[:10]:  # Show first 10
        print(f"  • {pdf_file.relative_to(DOCUMENTS_DIR)}")
    if len(pdf_files) > 10:
        print(f"  ... and {len(pdf_files) - 10} more")

    print("\n" + "-" * 60)

    # Ask for confirmation
    response = input("\nProceed with ingestion? (yes/no): ").strip().lower()
    if response not in ['yes', 'y']:
        print("\n❌ Ingestion cancelled")
        return

    print("\n" + "-" * 60)
    print("Starting document ingestion...")
    print("-" * 60 + "\n")

    try:
        # Initialize processor
        processor = DocumentProcessor()

        # Check if vector store exists
        force_refresh = False
        if VECTOR_DB_DIR.exists():
            print("⚠️  Existing vector store found")
            response = input("Recreate vector store? (yes/no): ").strip().lower()
            force_refresh = response in ['yes', 'y']

        # Ingest documents
        print("\n📚 Processing documents...")
        vector_store = processor.ingest_documents(force_refresh=force_refresh)

        if vector_store:
            print("\n" + "=" * 60)
            print("✅ Document ingestion completed successfully!")
            print("=" * 60)
            print(f"\n📊 Statistics:")
            print(f"  • PDF files processed: {len(pdf_files)}")
            print(f"  • Vector store location: {VECTOR_DB_DIR}")
            print(f"  • Status: Ready for use")

            print("\n🚀 Next steps:")
            print("  1. Run Telegram bot: python telegram_bot.py")
            print("  2. OR run web interface: streamlit run streamlit_app.py")
            print("  3. Start asking questions!")

        else:
            print("\n❌ Document ingestion failed")
            print("Please check the logs for errors")

    except Exception as e:
        logger.error(f"Ingestion error: {e}")
        print(f"\n❌ Error during ingestion: {e}")
        print("\nPlease check:")
        print("  1. PDF files are not corrupted")
        print("  2. PDF files contain selectable text (not scanned images)")
        print("  3. You have sufficient disk space")
        return 1

    print("\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
