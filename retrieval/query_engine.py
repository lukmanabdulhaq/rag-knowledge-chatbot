import os
import json
from dotenv import load_dotenv
load_dotenv()

import voyageai
from pinecone import Pinecone


def query_pinecone(query: str, namespace: str = "company-docs", top_k: int = 5) -> list:
    vo = voyageai.Client(api_key=os.getenv("VOYAGE_API_KEY"))
    query_embedding = vo.embed([query], model="voyage-3", input_type="query").embeddings[0]

    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(os.getenv("PINECONE_INDEX_NAME", "rag-knowledge-dev"))

    results = index.query(
        vector=query_embedding,
        top_k=top_k,
        namespace=namespace,
        include_metadata=True,
        include_values=False,
    )

    matches = []
    for m in results.matches:
        node_content = m.metadata.get("_node_content", "{}")
        parsed = json.loads(node_content)
        text = parsed.get("text", "")
        matches.append({"score": m.score, "text": text, "id": m.id})

    print(f"✅ Retrieved {len(matches)} chunks")
    return matches
