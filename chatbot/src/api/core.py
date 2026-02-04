"""
Modelos y utilidades centrales del chatbot
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ChatRequest(BaseModel):
    query: str = Field(..., description="Pregunta o consulta del usuario")
    session_id: Optional[str] = Field(None, description="ID de sesión (se genera si no existe)")
    filters: Optional[dict] = Field(None, description="Filtros opcionales (géneros, precio, año)")

class GameRecommendation(BaseModel):
    name: str
    genres: List[str]
    price: Optional[float]
    description: Optional[str]
    relevance_score: Optional[float] = None

class ChatResponse(BaseModel):
    response: str = Field(..., description="Recomendación generada por el LLM")
    session_id: str = Field(..., description="ID de la sesión")
    retrieved_games: List[GameRecommendation] = Field(..., description="Juegos que alimentaron la respuesta")
    message_count: int = Field(..., description="Total de mensajes en esta sesión")
    timestamp: str = Field(..., description="Timestamp de la respuesta")

class HealthResponse(BaseModel):
    status: str
    version: str
    components: dict = Field(default={
        "api": "operational",
        "retriever": "pending",
        "llm": "pending",
        "database": "pending"
    }, description="Estado de componentes")

class SessionStatsResponse(BaseModel):
    session_id: str
    created_at: str
    last_activity: str
    message_count: int
    user_messages: int
    assistant_messages: int
