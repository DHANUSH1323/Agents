"""Chroma persistent store + ingestion pipeline for document RAG."""
from pathlib import Path

import chromadb
from llama_index.core.ingestion import IngestionPipeline
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore

BASE_DIR = Path(__file__).resolve().parent
CHROMA_DIR = BASE_DIR / "chroma_db"
DOCUMENTS_DIR = BASE_DIR / "documents"

EMBEDDING_MODEL_NAME = "BAAI/bge-small-en-v1.5"


def get_chroma_vector_store(collection_name: str = "claims") -> ChromaVectorStore:
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    collection = client.get_or_create_collection(name=collection_name)
    return ChromaVectorStore(chroma_collection=collection)


def build_ingestion_pipeline(vector_store: ChromaVectorStore) -> IngestionPipeline:
    return IngestionPipeline(
        transformations=[
            SentenceSplitter(chunk_size=512, chunk_overlap=64),
            HuggingFaceEmbedding(model_name=EMBEDDING_MODEL_NAME),
        ],
        vector_store=vector_store,
    )
