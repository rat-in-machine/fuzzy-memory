"""
FastAPI Application - Chatbot RAG
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import logging

from config.settings import settings

logger = logging.getLogger(__name__)


# Modelos de datos
class ChatRequest(BaseModel):
    query: str
    session_id: Optional[str] = None
    filters: Optional[dict] = None
    

class ChatResponse(BaseModel):
    response: str
    session_id: str
    retrieved_games: List[dict]
    


class HealthResponse(BaseModel):
    status: str
    version: str


# Crear aplicación
app = FastAPI(
    title="Videogames Recommender Chatbot",
    description="RAG-based chatbot para recomendación de videojuegos",
    version="0.1.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Endpoints
@app.get("/", response_model=HealthResponse)
async def root():
    """Health check"""
    return {
        "status": "healthy",
        "version": "0.1.0"
    }


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Endpoint principal de chat
    
    Recibe query del usuario y devuelve recomendación
    """
    try:
        logger.info(f"Recibida consulta: '{request.query}'")
        
        # TODO: Implementar lógica completa
        # 1. Retrieval de juegos relevantes
        # 2. Generación de respuesta con LLM
        # 3. Gestión de sesión
        
        # Placeholder
        return {
            "response": "Sistema en desarrollo. Próximamente disponible.",
            "session_id": request.session_id or "session_001",
            "retrieved_games": []
        }
        
    except Exception as e:
        logger.error(f"Error en /chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/chat/reset")
async def reset_chat(session_id: str):
    """Resetea la memoria de una sesión de chat"""
    try:
        logger.info(f"Reseteando sesión: {session_id}")
        # TODO: Implementar limpieza de memoria
        return {"message": "Sesión reseteada", "session_id": session_id}
        
    except Exception as e:
        logger.error(f"Error en /chat/reset: {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Iniciando servidor en {settings.api_host}:{settings.api_port}")
    
    uvicorn.run(
        "main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.api_reload
    )
