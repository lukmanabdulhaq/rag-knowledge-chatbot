import os
import requests
from dotenv import load_dotenv
load_dotenv()

from retrieval.query_engine import query_pinecone
from retrieval.reranker import rerank
from retrieval.context_builder import build_context


def answer(query: str, namespace: str = "company-docs", model: str = "llama3.2") -> str:
    matches = query_pinecone(query, namespace=namespace)
    reranked = rerank(query, matches)
    context = build_context(reranked)

    prompt = f"You are a helpful assistant. Answer using only the context below. If the answer is not in the context, say so.\n\nContext:\n{context}\n\nQuestion: {query}"

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={"model": model, "prompt": prompt, "stream": False},
    )

    result = response.json()["response"]
    print("✅ Generated answer via Ollama")
    return result
