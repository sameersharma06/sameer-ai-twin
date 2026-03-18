# knowledge/retriever.py — Layer 3: RAG Query Engine (fully local)
import os
import chromadb
from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

CHROMA_PATH = "data/chroma_db"

# Fully local — no OpenAI, no internet
Settings.embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")
Settings.llm = None


def query(question: str) -> str:
    if not os.path.exists(CHROMA_PATH):
        return "empty"

    try:
        client       = chromadb.PersistentClient(path=CHROMA_PATH)
        collection   = client.get_or_create_collection("sameer_knowledge")

        if collection.count() == 0:
            return "empty"

        vector_store = ChromaVectorStore(chroma_collection=collection)
        index        = VectorStoreIndex.from_vector_store(vector_store)

        # Retrieve directly — no LLM needed
        retriever = VectorIndexRetriever(index=index, similarity_top_k=1)
        nodes     = retriever.retrieve(question)

        if not nodes:
            return "empty"

        # Combine top results into one context string
        result = "\n\n".join([node.text for node in nodes])
        return result.strip()

    except Exception:
        return "empty"