"""
Document Processing and Ingestion System
Handles PDFs, Markdown files and creates vector embeddings
"""

import os
import re
from pathlib import Path
from typing import List, Dict, Optional
from loguru import logger

# Fixed imports for LangChain 1.0+
from langchain_community.document_loaders import PyPDFLoader, TextLoader
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
        - class_10_science_chapter_5.pdf
        - polytechnic_electrical_semester_2.pdf
        """
        metadata = {}

        # Extract class/grade
        class_match = re.search(r'class[_\s]?(\d+)', filename, re.IGNORECASE)
        if class_match:
            metadata['class'] = f"Class {class_match.group(1)}"
            metadata['level'] = 'school'

        # Extract semester
        sem_match = re.search(r'semester[_\s]?(\d+)', filename, re.IGNORECASE)
        if sem_match:
            metadata['semester'] = f"Semester {sem_match.group(1)}"

        # Extract subject
        subjects = [
            'mathematics', 'math', 'science', 'physics', 'chemistry',
            'biology', 'english', 'hindi', 'social', 'history', 'geography',
            'economics', 'political', 'computer', 'electrical', 'mechanical',
            'civil', 'electronics'
        ]
        for subject in subjects:
            if subject in filename.lower():
                metadata['subject'] = subject.title()
                break

        # Extract chapter
        chapter_match = re.search(r'chapter[_\s]?(\d+)', filename, re.IGNORECASE)
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

    def load_documents(self, category: Optional[str] = None) -> List[Document]:
        """
        Load documents from the documents directory
        Supports: PDF, Markdown (.md), Text (.txt)

        Args:
            category: Optional category to load (textbooks, knowledge_base, etc.)

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
        file_extensions = ["*.pdf", "*.md", "*.txt"]
        
        # Process each file type
        for ext_pattern in file_extensions:
            for file_path in doc_path.rglob(ext_pattern):
                try:
                    logger.debug(f"Processing: {file_path.name}")
                    
                    # Select appropriate loader based on file extension
                    if file_path.suffix.lower() == '.pdf':
                        loader = PyPDFLoader(str(file_path))
                    elif file_path.suffix.lower() == '.md':
                        try:
                            loader = UnstructuredMarkdownLoader(str(file_path))
                        except Exception as e:
                            logger.warning(f"UnstructuredMarkdownLoader failed for {file_path.name}, using TextLoader: {e}")
                            loader = TextLoader(str(file_path), encoding='utf-8')
                    elif file_path.suffix.lower() == '.txt':
                        loader = TextLoader(str(file_path), encoding='utf-8')
                    else:
                        logger.warning(f"Unsupported file type: {file_path.suffix}")
                        continue

                    # Load documents
                    try:
                        documents = loader.load()
                    except Exception as e:
                        logger.error(f"Error loading {file_path.name}: {e}")
                        # Try with different encoding for text files
                        if file_path.suffix.lower() in ['.md', '.txt']:
                            try:
                                loader = TextLoader(str(file_path), encoding='latin-1')
                                documents = loader.load()
                                logger.info(f"Successfully loaded {file_path.name} with latin-1 encoding")
                            except Exception as e2:
                                logger.error(f"Failed to load {file_path.name} with alternative encoding: {e2}")
                                continue
                        else:
                            continue

                    # Extract metadata
                    file_metadata = self.extract_metadata_from_filename(file_path.stem)
                    category = self.get_category_from_path(file_path)

                    # Add metadata to each document
                    for doc in documents:
                        doc.metadata.update({
                            'source': file_path.name,
                            'file_type': file_path.suffix[1:],  # Remove the dot
                            'category': category,
                            **file_metadata
                        })

                    all_documents.extend(documents)
                    logger.info(f"✓ Loaded {len(documents)} page(s) from {file_path.name}")

                except Exception as e:
                    logger.error(f"✗ Error processing {file_path.name}: {e}")
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
