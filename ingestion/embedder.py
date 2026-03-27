import os
from typing import List

import voyageai
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core import Settings
from llama_index.core.schema import TextNode


def embed_nodes(nodes: List[TextNode], provider: str = "voyage") -> List[TextNode]:
    texts = [node.get_content() for node in nodes]

    if provider == "openai":
        embed_model = OpenAIEmbedding(
            model="text-embedding-3-small",
            api_key=os.getenv("OPENAI_API_KEY"),
            embed_batch_size=100,
        )
        Settings.embed_model = embed_model
        embeddings = embed_model.get_text_embedding_batch(texts, show_progress=True)

    else:
        vo = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
        result = vo.embed(texts, model="voyage-3", input_type="document")
        embeddings = result.embeddings

    for node, embedding in zip(nodes, embeddings):
        node.embedding = embedding

    print(f"✅ Embedded {len(nodes)} chunks via {provider}")
    return nodes
