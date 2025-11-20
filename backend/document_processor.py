"""
Document Processing and Ingestion System
Handles PDFs, Markdown, and JSON files and creates vector embeddings
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Optional
from loguru import logger

from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

import sys
sys.path.append(str(Path(__file__).parent.parent))
from utils.config import settings, DOCUMENTS_DIR, VECTOR_DB_DIR, DOCUMENT_CATEGORIES


class DocumentProcessor:
    """Process and index documents for RAG system"""

    def __init__(self):
        self.documents_dir = DOCUMENTS_DIR
        self.vector_db_path = str(VECTOR_DB_DIR)

        # Initialize text splitter
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", "। ", "| ", " ", ""]
        )

        # Initialize embeddings
        logger.info(f"Loading embedding model: {settings.embedding_model}")
        self.embeddings = HuggingFaceEmbeddings(
            model_name=settings.embedding_model,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )

        self.vector_store: Optional[Chroma] = None

    def extract_metadata_from_filename(self, filename: str) -> Dict[str, str]:
        """
        Extract metadata from filename patterns like:
        - class_8_mathematics.pdf
        - class_10_maths (1).pdf  <- Handle numbered copies
        - class_10_science_chapter_5.pdf
        - polytechnic_electrical_semester_2.pdf
        """
        metadata = {}

        # Clean filename - remove copy numbers like (1), (2), etc.
        clean_filename = re.sub(r'\s*\(\d+\)', '', filename)

        # Extract class/grade
        class_match = re.search(r'class[_\s]?(\d+)', clean_filename, re.IGNORECASE)
        if class_match:
            metadata['class'] = f"Class {class_match.group(1)}"
            metadata['level'] = 'school'

        # Extract semester
        sem_match = re.search(r'semester[_\s]?(\d+)', clean_filename, re.IGNORECASE)
        if sem_match:
            metadata['semester'] = f"Semester {sem_match.group(1)}"

        # Extract subject (expanded list with abbreviations)
        subjects_map = {
            'mathematics': 'Mathematics',
            'maths': 'Mathematics',
            'math': 'Mathematics',
            'science': 'Science',
            'physics': 'Physics',
            'chemistry': 'Chemistry',
            'biology': 'Biology',
            'english': 'English',
            'hindi': 'Hindi',
            'social': 'Social Science',
            'history': 'History',
            'geography': 'Geography',
            'economics': 'Economics',
            'political': 'Political Science',
            'computer': 'Computer Science',
            'electrical': 'Electrical Engineering',
            'mechanical': 'Mechanical Engineering',
            'civil': 'Civil Engineering',
            'electronics': 'Electronics',
            'accountancy': 'Accountancy',
            'commerce': 'Commerce',
            'business': 'Business Studies'
        }

        for key, subject_name in subjects_map.items():
            if key in clean_filename.lower():
                metadata['subject'] = subject_name
                break

        # Extract chapter
        chapter_match = re.search(r'chapter[_\s]?(\d+)', clean_filename, re.IGNORECASE)
        if chapter_match:
            metadata['chapter'] = f"Chapter {chapter_match.group(1)}"

        return metadata

    def get_category_from_path(self, file_path: Path) -> str:
        """Determine document category from file path"""
        path_parts = file_path.parts
        for category in DOCUMENT_CATEGORIES.keys():
            if category in path_parts:
                return category
        return "general"

    def is_valid_document(self, documents: List[Document], filename: str) -> bool:
        """
        Check if document has meaningful content (not just cover page or empty)

        Args:
            documents: List of pages from PDF
            filename: Name of the file

        Returns:
            True if document should be included, False if should be skipped
        """
        # Skip if no pages
        if not documents:
            logger.warning(f"Skipping {filename}: No pages found")
            return False

        # Skip if only 1-2 pages (likely just cover)
        if len(documents) <= 2:
            # Check if these pages have substantial content
            total_text = "".join([doc.page_content for doc in documents])
            # If less than 200 characters total, it's likely just a cover page
            if len(total_text.strip()) < 200:
                logger.warning(f"Skipping {filename}: Only {len(total_text)} chars (likely cover page)")
                return False

        # Check first page content for cover page indicators
        first_page = documents[0].page_content.lower()
        cover_indicators = [
            'cover page',
            'government of rajasthan',
            'राजस्थान सरकार',
            'department of education'
        ]

        # If first page is very short and contains cover indicators
        if len(first_page.strip()) < 300:
            if any(indicator in first_page for indicator in cover_indicators):
                # But if PDF has many pages, it's still valid (cover + content)
                if len(documents) > 3:
                    logger.info(f"Including {filename}: Has cover but {len(documents)} total pages")
                    return True
                else:
                    logger.warning(f"Skipping {filename}: Appears to be cover-only PDF")
                    return False

        return True

    def load_markdown_file(self, file_path: Path) -> List[Document]:
        """
        Load a markdown file and convert it to Document objects

        Args:
            file_path: Path to the markdown file

        Returns:
            List of Document objects
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract metadata
            file_metadata = self.extract_metadata_from_filename(file_path.stem)
            category = self.get_category_from_path(file_path)

            # Create document with metadata
            doc = Document(
                page_content=content,
                metadata={
                    'source': file_path.name,
                    'category': category,
                    'file_type': 'markdown',
                    **file_metadata
                }
            )

            logger.info(f"Loaded markdown file: {file_path.name}")
            return [doc]

        except Exception as e:
            logger.error(f"Error loading markdown file {file_path.name}: {e}")
            return []

    def load_json_file(self, file_path: Path) -> List[Document]:
        """
        Load a JSON file and convert it to Document objects

        Args:
            file_path: Path to the JSON file

        Returns:
            List of Document objects
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Convert JSON to readable text format
            content = json.dumps(data, indent=2, ensure_ascii=False)

            # Also create a more readable version
            readable_content = self._json_to_readable_text(data)

            # Extract metadata
            file_metadata = self.extract_metadata_from_filename(file_path.stem)
            category = self.get_category_from_path(file_path)

            # Create document with metadata
            doc = Document(
                page_content=readable_content,
                metadata={
                    'source': file_path.name,
                    'category': category,
                    'file_type': 'json',
                    **file_metadata
                }
            )

            logger.info(f"Loaded JSON file: {file_path.name}")
            return [doc]

        except Exception as e:
            logger.error(f"Error loading JSON file {file_path.name}: {e}")
            return []

    def _json_to_readable_text(self, data: dict, level: int = 0) -> str:
        """
        Convert JSON data to readable text format for better RAG retrieval

        Args:
            data: JSON data (dict or list)
            level: Current nesting level for indentation

        Returns:
            Readable text representation
        """
        lines = []
        indent = "  " * level

        if isinstance(data, dict):
            for key, value in data.items():
                # Format key nicely
                formatted_key = key.replace('_', ' ').title()

                if isinstance(value, dict):
                    lines.append(f"{indent}{formatted_key}:")
                    lines.append(self._json_to_readable_text(value, level + 1))
                elif isinstance(value, list):
                    lines.append(f"{indent}{formatted_key}:")
                    for item in value:
                        if isinstance(item, (dict, list)):
                            lines.append(self._json_to_readable_text(item, level + 1))
                        else:
                            lines.append(f"{indent}  - {item}")
                else:
                    lines.append(f"{indent}{formatted_key}: {value}")
        elif isinstance(data, list):
            for item in data:
                if isinstance(item, (dict, list)):
                    lines.append(self._json_to_readable_text(item, level))
                else:
                    lines.append(f"{indent}- {item}")
        else:
            lines.append(f"{indent}{data}")

        return "\n".join(lines)

    def load_documents(self, category: Optional[str] = None) -> List[Document]:
        """
        Load documents from the documents directory (PDF, Markdown, JSON)

        Args:
            category: Optional category to load (textbooks, admissions, etc.)

        Returns:
            List of Document objects
        """
        if category:
            doc_path = self.documents_dir / category
        else:
            doc_path = self.documents_dir

        if not doc_path.exists():
            logger.warning(f"Documents directory not found: {doc_path}")
            return []

        logger.info(f"Loading documents from: {doc_path}")

        all_documents = []

        # Load PDF files
        skipped_count = 0
        for pdf_file in doc_path.rglob("*.pdf"):
            try:
                logger.debug(f"Processing PDF: {pdf_file.name}")

                # Load PDF
                loader = PyPDFLoader(str(pdf_file))
                documents = loader.load()

                # Validate document has meaningful content
                if not self.is_valid_document(documents, pdf_file.name):
                    skipped_count += 1
                    continue

                # Extract metadata
                file_metadata = self.extract_metadata_from_filename(pdf_file.stem)
                category = self.get_category_from_path(pdf_file)

                # Add metadata to each document
                for doc in documents:
                    doc.metadata.update({
                        'source': pdf_file.name,
                        'category': category,
                        'file_type': 'pdf',
                        **file_metadata
                    })

                all_documents.extend(documents)
                logger.info(f"Loaded {len(documents)} pages from {pdf_file.name}")

            except Exception as e:
                logger.error(f"Error loading {pdf_file.name}: {e}")
                continue

        if skipped_count > 0:
            logger.info(f"Skipped {skipped_count} PDFs (cover pages or low content)")

        # Load Markdown files
        for md_file in doc_path.rglob("*.md"):
            try:
                logger.debug(f"Processing Markdown: {md_file.name}")
                documents = self.load_markdown_file(md_file)
                all_documents.extend(documents)

            except Exception as e:
                logger.error(f"Error loading {md_file.name}: {e}")
                continue

        # Load JSON files
        for json_file in doc_path.rglob("*.json"):
            try:
                logger.debug(f"Processing JSON: {json_file.name}")
                documents = self.load_json_file(json_file)
                all_documents.extend(documents)

            except Exception as e:
                logger.error(f"Error loading {json_file.name}: {e}")
                continue

        logger.info(f"Total documents loaded: {len(all_documents)}")
        return all_documents

    def process_documents(self, documents: List[Document]) -> List[Document]:
        """
        Split documents into chunks

        Args:
            documents: List of documents to process

        Returns:
            List of chunked documents
        """
        logger.info(f"Splitting {len(documents)} documents into chunks...")
        chunks = self.text_splitter.split_documents(documents)
        logger.info(f"Created {len(chunks)} chunks")
        return chunks

    def create_vector_store(self, documents: List[Document]) -> Chroma:
        """
        Create vector store from documents

        Args:
            documents: List of document chunks

        Returns:
            Chroma vector store
        """
        logger.info("Creating vector store...")

        # Create directory if it doesn't exist
        VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)

        # Create vector store
        vector_store = Chroma.from_documents(
            documents=documents,
            embedding=self.embeddings,
            persist_directory=self.vector_db_path
        )

        logger.info(f"Vector store created with {len(documents)} documents")
        return vector_store

    def load_vector_store(self) -> Optional[Chroma]:
        """
        Load existing vector store

        Returns:
            Chroma vector store or None if doesn't exist
        """
        if not VECTOR_DB_DIR.exists():
            logger.warning("Vector store directory not found")
            return None

        try:
            logger.info("Loading existing vector store...")
            vector_store = Chroma(
                persist_directory=self.vector_db_path,
                embedding_function=self.embeddings
            )
            logger.info("Vector store loaded successfully")
            return vector_store
        except Exception as e:
            logger.error(f"Error loading vector store: {e}")
            return None

    def ingest_documents(self, force_refresh: bool = False) -> Chroma:
        """
        Main ingestion pipeline

        Args:
            force_refresh: If True, recreate vector store even if exists

        Returns:
            Chroma vector store
        """
        # Try to load existing vector store
        if not force_refresh:
            self.vector_store = self.load_vector_store()
            if self.vector_store:
                return self.vector_store

        # Load and process documents
        logger.info("Starting document ingestion pipeline...")
        documents = self.load_documents()

        if not documents:
            logger.warning("No documents found to ingest!")
            return None

        # Process documents
        chunks = self.process_documents(documents)

        # Create vector store
        self.vector_store = self.create_vector_store(chunks)

        logger.info("Document ingestion completed successfully!")
        return self.vector_store

    def add_documents(self, file_paths: List[str]) -> bool:
        """
        Add new documents to existing vector store

        Args:
            file_paths: List of PDF file paths to add

        Returns:
            True if successful
        """
        try:
            # Load existing vector store
            if not self.vector_store:
                self.vector_store = self.load_vector_store()

            if not self.vector_store:
                logger.error("No existing vector store found. Run ingest_documents first.")
                return False

            # Load new documents
            all_documents = []
            for file_path in file_paths:
                loader = PyPDFLoader(file_path)
                documents = loader.load()

                # Add metadata
                file_metadata = self.extract_metadata_from_filename(Path(file_path).stem)
                for doc in documents:
                    doc.metadata.update(file_metadata)

                all_documents.extend(documents)

            # Process and add to vector store
            chunks = self.process_documents(all_documents)
            self.vector_store.add_documents(chunks)

            logger.info(f"Added {len(chunks)} chunks from {len(file_paths)} documents")
            return True

        except Exception as e:
            logger.error(f"Error adding documents: {e}")
            return False

    def search(self, query: str, k: int = 4) -> List[Document]:
        """
        Search vector store for relevant documents

        Args:
            query: Search query
            k: Number of results to return

        Returns:
            List of relevant documents
        """
        if not self.vector_store:
            self.vector_store = self.load_vector_store()

        if not self.vector_store:
            logger.warning("Vector store not available")
            return []

        results = self.vector_store.similarity_search(query, k=k)
        return results


if __name__ == "__main__":
    # Test document processing
    processor = DocumentProcessor()

    print("YuvaSaarthi - Document Processor")
    print("=" * 60)

    # Ingest documents
    vector_store = processor.ingest_documents()

    if vector_store:
        # Test search
        test_query = "What is Pythagoras theorem?"
        print(f"\nTest Query: {test_query}")
        results = processor.search(test_query, k=2)

        for i, doc in enumerate(results, 1):
            print(f"\n--- Result {i} ---")
            print(f"Source: {doc.metadata.get('source', 'Unknown')}")
            print(f"Content: {doc.page_content[:200]}...")
