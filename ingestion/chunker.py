# ingestion/chunker.py
from typing import List

from llama_index.core import Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core.schema import Document, TextNode


def chunk_documents(
    documents: List[Document],
    chunk_size: int = 300,
    chunk_overlap: int = 20,
) -> List[TextNode]:
    """
    Split documents into semantic chunks.
    Target: 200-400 tokens per chunk, 20-token overlap.
    """
    splitter = SentenceSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        paragraph_separator="\n\n",
    )

    nodes = splitter.get_nodes_from_documents(documents, show_progress=True)
    print(f"✅ Created {len(nodes)} chunks from {len(documents)} document(s)")
    return nodes
