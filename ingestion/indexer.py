import os
from typing import List, Optional

from pinecone import Pinecone, ServerlessSpec
from llama_index.core.schema import TextNode
from llama_index.vector_stores.pinecone import PineconeVectorStore
from llama_index.core import StorageContext, VectorStoreIndex


def get_pinecone_index():
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = os.getenv("PINECONE_INDEX_NAME", "rag-knowledge-dev")

    existing = [i.name for i in pc.list_indexes()]
    if index_name not in existing:
        print(f"Creating index: {index_name}")
        pc.create_index(
            name=index_name,
            dimension=1024,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1"),
        )

    return pc.Index(index_name)


def upsert_nodes(nodes: List[TextNode], namespace: Optional[str] = "default") -> None:
    index = get_pinecone_index()
    vector_store = PineconeVectorStore(pinecone_index=index, namespace=namespace)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    VectorStoreIndex(
        nodes,
        storage_context=storage_context,
        show_progress=True,
    )
    print(f"✅ Upserted {len(nodes)} chunks to namespace: {namespace}")


def run_ingestion_pipeline(
    source_dir: str,
    namespace: str = "default",
    chunk_size: int = 300,
    chunk_overlap: int = 20,
    provider: str = "voyage",
) -> None:
    from ingestion.loader import load_documents
    from ingestion.chunker import chunk_documents
    from ingestion.embedder import embed_nodes

    print(f"\n🚀 Starting ingestion pipeline for: {source_dir}")
    documents = load_documents(source_dir)
    nodes = chunk_documents(documents, chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    nodes = embed_nodes(nodes, provider=provider)
    upsert_nodes(nodes, namespace=namespace)
    print(f"\n✅ Pipeline complete. {len(nodes)} chunks in namespace '{namespace}'")
