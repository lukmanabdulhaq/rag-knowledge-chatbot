import os
from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI
from pydantic import BaseModel
from agent.graph import answer

app = FastAPI(title="RAG Knowledge Chatbot", version="1.0.0")


class QueryRequest(BaseModel):
    query: str
    namespace: str = "company-docs"


class QueryResponse(BaseModel):
    query: str
    answer: str
    namespace: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/chat", response_model=QueryResponse)
def chat(request: QueryRequest):
    response = answer(request.query, namespace=request.namespace)
    return QueryResponse(query=request.query, answer=response, namespace=request.namespace)
