import os
import cohere
from typing import List


def rerank(query: str, matches: List[dict], top_n: int = 3) -> List[dict]:
    if not matches:
        return []

    co = cohere.ClientV2(api_key=os.getenv("COHERE_API_KEY"))
    docs = [m["text"] for m in matches]

    response = co.rerank(
        model="rerank-v3.5",
        query=query,
        documents=docs,
        top_n=top_n,
    )

    reranked = []
    for r in response.results:
        match = matches[r.index]
        match["rerank_score"] = r.relevance_score
        reranked.append(match)

    print(f"✅ Reranked to top {len(reranked)} chunks")
    return reranked
