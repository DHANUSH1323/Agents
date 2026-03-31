"""Ingest documents into Chroma, query with Hugging Face Inference API, optional faithfulness eval + Phoenix tracing."""
from __future__ import annotations

import os
import sys
from pathlib import Path

# Allow `python document_RAG/document_rag.py` from repo root
_DOC_ROOT = Path(__file__).resolve().parent
if str(_DOC_ROOT) not in sys.path:
    sys.path.insert(0, str(_DOC_ROOT))

from dotenv import load_dotenv
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex
from llama_index.core.evaluation import FaithfulnessEvaluator
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.huggingface_api import HuggingFaceInferenceAPI

from storing import (
    BASE_DIR,
    DOCUMENTS_DIR,
    EMBEDDING_MODEL_NAME,
    build_ingestion_pipeline,
    get_chroma_vector_store,
)

load_dotenv(BASE_DIR.parent / ".env")


def load_documents():
    if not DOCUMENTS_DIR.is_dir():
        DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    if not any(DOCUMENTS_DIR.iterdir()):
        raise FileNotFoundError(
            f"Add files under {DOCUMENTS_DIR} (e.g. sample.txt or PDFs). "
            "A sample text file is included for local testing."
        )
    return SimpleDirectoryReader(input_dir=str(DOCUMENTS_DIR)).load_data()


def maybe_setup_phoenix() -> None:
    key = os.environ.get("PHOENIX_API_KEY")
    if not key:
        return
    try:
        os.environ["OTEL_EXPORTER_OTLP_HEADERS"] = f"api_key={key}"
        from llama_index.core import set_global_handler

        set_global_handler("arize_phoenix", endpoint="https://llamatrace.com/v1/traces")
    except Exception:
        pass


def main() -> None:
    maybe_setup_phoenix()

    documents = load_documents()
    vector_store = get_chroma_vector_store()
    pipeline = build_ingestion_pipeline(vector_store)
    pipeline.run(documents=documents, show_progress=True)

    embed_model = HuggingFaceEmbedding(model_name=EMBEDDING_MODEL_NAME)
    index = VectorStoreIndex.from_vector_store(vector_store, embed_model=embed_model)

    llm = HuggingFaceInferenceAPI(
        model_name=os.environ.get("HF_LLM_MODEL", "Qwen/Qwen2.5-Coder-7B-Instruct"),
        provider="hf-inference",
        token=os.environ.get("HF_TOKEN"),
    )
    query_engine = index.as_query_engine(llm=llm, response_mode="tree_summarize")

    question = (
        "What battles took place in New York City in the American Revolution? "
        "Answer from the provided context."
    )
    response = query_engine.query(question)
    print(response)

    evaluator = FaithfulnessEvaluator(llm=llm)
    eval_result = evaluator.evaluate_response(response=response)
    print("Faithfulness passing:", eval_result.passing)


if __name__ == "__main__":
    main()
