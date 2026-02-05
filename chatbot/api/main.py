"""
FastAPI Application - Chatbot RAG para Recomendación de Videojuegos
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.api.endpoints import health, search, chat

app = FastAPI(
    title="Videogames Recommender Chatbot",
    description="RAG-based chatbot para recomendación de videojuegos con memoria conversacional",
    version="0.1.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(search.router)
app.include_router(chat.router)

