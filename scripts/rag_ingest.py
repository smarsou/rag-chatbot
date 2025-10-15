"""
Script to ingest PDF documents into a vector store for RAG pipeline.
"""
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))
from rag.loaders import PDFLoader
from rag.splitters import DocumentSplitter
from rag.vectorstores import MyVectorStoreInterface
from rag.embeddings import MyEmbedding
from rag.pipelines import RAGIngestionPipeline
from dotenv import load_dotenv
load_dotenv()

# Initialize components
loader = PDFLoader()
splitter = DocumentSplitter(chunk_size=1000, chunk_overlap=200)
embedding = MyEmbedding(api_base=os.getenv("EMBEDDING_API_BASE"))
vector_store = MyVectorStoreInterface(embedding=embedding, connection=os.getenv("VECTOR_DB_CONNECTION"), collection_name=os.getenv("VECTOR_DB_COLLECTION"))

# Create and run ingestion pipeline
ingestion_pipeline = RAGIngestionPipeline(loader, splitter, vector_store)
ingestion_pipeline.ingest("../rag/data/pdf/PFE.pdf", "../rag/data/pdf/PI.pdf")