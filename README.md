# RAG Knowledge-Base Chatbot

A production-grade Retrieval-Augmented Generation (RAG) API that ingests documents, stores them in a vector database, and answers questions with cited context.

## Architecture
```
Documents → Chunk → Embed (Voyage-3) → Pinecone → Query → Rerank (Cohere) → LLM → API
```

## Stack

| Layer | Tool |
|-------|------|
| Embeddings | Voyage-3 (Anthropic) or text-embedding-3-small (OpenAI) |
| Vector DB | Pinecone Serverless |
| Reranking | Cohere rerank-v3.5 |
| LLM | Claude Sonnet / Llama 3.2 (Ollama) |
| API | FastAPI |
| Container | Docker |

## Metrics

- p95 retrieval latency: < 200ms
- Faithfulness score: > 0.85 (RAGAS)
- Supports 10K+ documents via Pinecone namespaces
- Multi-tenant via namespace isolation

## Quickstart
```bash
git clone https://github.com/yourusername/rag-knowledge-chatbot
cd rag-knowledge-chatbot
cp .env.example .env  # fill in your keys
docker build -t rag-knowledge-chatbot .
docker run -p 8000:8000 rag-knowledge-chatbot
```

## Ingest Documents
```bash
uv run python -c "
from ingestion.indexer import run_ingestion_pipeline
run_ingestion_pipeline('./docs', namespace='your-namespace')
"
```

## Query the API
```bash
curl -X POST http://localhost:8000/chat \
  -H 'Content-Type: application/json' \
  -d '{"query": "What is the refund policy?", "namespace": "company-docs"}'
```

## Project Structure
```
ingestion/    # load, chunk, embed, upsert pipeline
retrieval/    # query, rerank, context assembly
agent/        # LLM generation layer
api/          # FastAPI endpoints
eval/         # RAGAS evaluation suite
infra/        # Docker, Terraform
```

## Embedding Providers

Supports both Voyage-3 (Anthropic) and OpenAI text-embedding-3-small.
Switch via the provider parameter in embed_nodes().
