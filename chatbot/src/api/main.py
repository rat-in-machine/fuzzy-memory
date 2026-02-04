"""
FastAPI Application - Chatbot RAG para Recomendación de Videojuegos

Caso de Uso:
- Usuario escribe pregunta natural sobre videojuegos (ej: "Recomendame juegos de acción épicos")
- Sistema recupera juegos relevantes de BD mediante búsqueda híbrida (vectorial + filtros)
- LLM genera recomendación personalizada con explicaciones
- Memoria conversacional mantiene contexto entre mensajes

Flujo:
1. Usuario inicia sesión con query
2. Retriever busca juegos relevantes (FAISS + MongoDB)
3. LLM genera recomendación con contexto
4. Respuesta se guarda en sesión para conversaciones futuras
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Optional, List
import logging
import sys
from datetime import datetime
from pathlib import Path

# Agregar el directorio padre al path para imports correctos
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from config.settings import settings
from .session_manager import SessionManager
from src.services.game_search import get_game_search

# Imports de componentes RAG (cuando estén disponibles)
# from src.retrieval.retriever import HybridRetriever
# from src.llm.chain import RecommendationChain

logger = logging.getLogger(__name__)

# =============================================================================
# MODELOS DE DATOS
# =============================================================================

class ChatRequest(BaseModel):
    """Request de chat del usuario"""
    query: str = Field(..., description="Pregunta o consulta del usuario")
    session_id: Optional[str] = Field(None, description="ID de sesión (se genera si no existe)")
    filters: Optional[dict] = Field(None, description="Filtros opcionales (géneros, precio, año)")
    
    class Config:
        example = {
            "query": "Quiero juegos de acción épicos con buenos gráficos",
            "session_id": "user_123",
            "filters": {
                "genres": ["Action", "RPG"],
                "max_price": 60,
                "min_year": 2020
            }
        }


class GameRecommendation(BaseModel):
    """Información de un juego recomendado"""
    name: str
    genres: List[str]
    price: Optional[float]
    description: Optional[str]
    relevance_score: Optional[float] = None


class ChatResponse(BaseModel):
    """Response del endpoint de chat"""
    response: str = Field(..., description="Recomendación generada por el LLM")
    session_id: str = Field(..., description="ID de la sesión")
    retrieved_games: List[GameRecommendation] = Field(..., description="Juegos que alimentaron la respuesta")
    message_count: int = Field(..., description="Total de mensajes en esta sesión")
    timestamp: str = Field(..., description="Timestamp de la respuesta")


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    components: dict = Field(
        default={
            "api": "operational",
            "retriever": "pending",
            "llm": "pending",
            "database": "pending"
        },
        description="Estado de componentes"
    )


class SessionStatsResponse(BaseModel):
    """Estadísticas de sesión"""
    session_id: str
    created_at: str
    last_activity: str
    message_count: int
    user_messages: int
    assistant_messages: int


# =============================================================================
# INICIALIZACIÓN DE APLICACIÓN
# =============================================================================

app = FastAPI(
    title="Videogames Recommender Chatbot",
    description="RAG-based chatbot para recomendación de videojuegos con memoria conversacional",
    version="0.1.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gestor de sesiones
session_manager = SessionManager(session_timeout_minutes=60)

# TODO: Inicializar componentes cuando estén listos
# retriever = HybridRetriever(vector_store, db_client)
# llm_chain = RecommendationChain()

logger.info("Aplicación de chatbot inicializada")


# =============================================================================
# ENDPOINTS
# =============================================================================

@app.get("/", response_model=HealthResponse, tags=["Health"])
async def root():
    """
    Health check del sistema
    
    Verifica el estado general de la aplicación y sus componentes
    """
    return {
        "status": "operational",
        "version": "0.1.0",
        "components": {
            "api": "operational",
            "retriever": "pending (awaiting FAISS + MongoDB)",
            "llm": "pending (awaiting OpenAI integration)",
            "database": "pending (awaiting MongoDB connection)"
        }
    }


@app.get("/test", tags=["Debug"])
async def test_endpoint():
    """Test endpoint simple"""
    return {"message": "Server is working"}


@app.get("/search-game", tags=["Search"])
async def search_game(name: str, limit: int = 5):
    """
    🔍 **BÚSQUEDA DE JUEGOS POR NOMBRE**
    
    Busca juegos en la BD de MongoDB por nombre y devuelve información completa
    
    **Parámetros:**
    - `name` (str): Nombre del juego a buscar (case-insensitive)
    - `limit` (int): Máximo de resultados (default: 5)
    
    **Ejemplo:**
    - GET /search-game?name=elden&limit=3
    
    **Respuesta:**
    ```json
    {
        "query": "elden",
        "found": 1,
        "results": [
            {
                "name": "ELDEN RING",
                "steam_id": 1245620,
                "price_retail_eur": "46.38",
                "price_keyshop_eur": "29.22",
                "status": "Available",
                "genres": ["Acción", "Rol"],
                "developer": "FromSoftware, Inc.",
                "metacritic": 94,
                "description": "Colaboramos con FromSoftware para traer..."
            }
        ]
    }
    ```
    """
    try:
        logger.info(f"Búsqueda: '{name}' (limit={limit})")
        game_search = get_game_search()
        games = game_search.search_by_name(name, limit=limit)
        
        if not games:
            return {"query": name, "found": 0, "results": [], "message": f"No se encontraron juegos con '{name}'"}
        
        results = []
        for game in games:
            retail = game.get("current_price_retail")
            keyshop = game.get("current_price_keyshop")
            
            # Determinar estado del precio
            if retail is None:
                price_status = "No disponible"
                price_retail = "N/A"
                price_keyshop = "N/A"
            elif retail == 0:
                price_status = "FREE-TO-PLAY"
                price_retail = "GRATIS"
                price_keyshop = "GRATIS"
            else:
                price_status = "Disponible"
                price_retail = f"{retail:.2f}"
                price_keyshop = f"{keyshop:.2f}" if keyshop and keyshop > 0 else "N/A"
            
            results.append({
                "name": game.get("name", "Desconocido"),
                "steam_id": game.get("steam_id"),
                "price_retail_eur": price_retail,
                "price_keyshop_eur": price_keyshop,
                "status": price_status,
                "genres": game.get("genres", []),
                "developer": game.get("developers", [None])[0] if game.get("developers") else "Desconocido",
                "metacritic": game.get("metacritic"),
                "description": game.get("description", "")[:150] + "..." if game.get("description") else "N/A"
            })
        
        logger.info(f"Búsqueda exitosa: {len(results)} resultados")
        
        return JSONResponse(
            content={
                "query": name,
                "found": len(results),
                "results": results
            },
            media_type="application/json; charset=utf-8"
        )
        
    except Exception as e:
        logger.error(f"Error en búsqueda: {str(e)}", exc_info=True)
        return JSONResponse(
            content={"error": str(e), "query": name},
            media_type="application/json; charset=utf-8"
        )


@app.get("/search-by-genre", tags=["Search"])
async def search_by_genre(genre: str, limit: int = 10):
    """
    🎮 **BÚSQUEDA DE JUEGOS POR GÉNERO**
    
    Busca juegos por género específico
    
    **Parámetros:**
    - `genre` (str): Género a buscar (Acción, RPG, Aventura, etc.)
    - `limit` (int): Máximo de resultados (default: 10)
    
    **Ejemplo:**
    - GET /search-by-genre?genre=Acción&limit=5
    """
    try:
        logger.info(f"Búsqueda por género: '{genre}' (limit={limit})")
        game_search = get_game_search()
        games = game_search.search_by_genre(genre, limit=limit)
        
        if not games:
            return JSONResponse(
                content={"genre": genre, "found": 0, "results": [], "message": f"No se encontraron juegos del género '{genre}'"},
                media_type="application/json; charset=utf-8"
            )
        
        results = []
        for game in games:
            retail = game.get("current_price_retail")
            keyshop = game.get("current_price_keyshop")
            
            if retail is None:
                price_retail = "N/A"
                price_keyshop = "N/A"
            elif retail == 0:
                price_retail = "GRATIS"
                price_keyshop = "GRATIS"
            else:
                price_retail = f"{retail:.2f}"
                price_keyshop = f"{keyshop:.2f}" if keyshop and keyshop > 0 else "N/A"
            
            results.append({
                "name": game.get("name"),
                "steam_id": game.get("steam_id"),
                "price_retail_eur": price_retail,
                "price_keyshop_eur": price_keyshop,
                "genres": game.get("genres", []),
                "metacritic": game.get("metacritic")
            })
        
        return JSONResponse(
            content={"genre": genre, "found": len(results), "results": results},
            media_type="application/json; charset=utf-8"
        )
        
    except Exception as e:
        logger.error(f"Error en búsqueda por género: {str(e)}", exc_info=True)
        return JSONResponse(
            content={"error": str(e), "genre": genre},
            media_type="application/json; charset=utf-8"
        )


@app.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    """
    🤖 **ENDPOINT PRINCIPAL DE CHAT**
    
    Procesa una consulta del usuario y devuelve recomendaciones personalizadas
    
    **Flujo:**
    1. Crear o recuperar sesión
    2. Guardar mensaje del usuario
    3. Recuperar juegos relevantes (HybridRetriever)
    4. Generar recomendación con LLM (RecommendationChain)
    5. Guardar respuesta en sesión
    6. Retornar respuesta + metadatos
    
    **Ejemplo de uso:**
    ```json
    POST /chat
    {
        "query": "Quiero un juego de rol épico con buena historia",
        "session_id": "user_123",
        "filters": {
            "genres": ["RPG"],
            "min_year": 2018
        }
    }
    ```
    
    **Respuesta:**
    ```json
    {
        "response": "Basado en tu preferencia... [recomendaciones detalladas]",
        "session_id": "user_123",
        "retrieved_games": [
            {
                "name": "Elden Ring",
                "genres": ["RPG", "Action"],
                "price": 59.99,
                "relevance_score": 0.92
            }
        ],
        "message_count": 1,
        "timestamp": "2026-02-04T12:34:56"
    }
    ```
    """
    try:
        logger.info(f"Consulta recibida: '{request.query}'")
        
        # 1. Gestión de sesión
        session_id = request.session_id
        if session_id is None:
            session_id = session_manager.create_session()
        else:
            session = session_manager.get_session(session_id)
            if session is None:
                session_id = session_manager.create_session(session_id)
        
        # 2. Guardar mensaje del usuario
        session_manager.add_message(
            session_id=session_id,
            role="user",
            content=request.query
        )
        
        # 3. Procesar consulta y buscar juegos
        game_search = get_game_search()
        query_lower = request.query.lower()
        
        # DETECCIÓN INTELIGENTE DE INTENCIÓN DE BÚSQUEDA
        # El sistema puede entender dos tipos de queries:
        # 1. Búsqueda por género: "Dame juegos de rol", "Strategy games"
        # 2. Búsqueda por nombre: "Elden Ring", "Minecraft"
        
        # Mapping de géneros (español e inglés, con y sin acentos)
        # Permite detectar intención incluso con variaciones idiomáticas y ortográficas
        genre_mapping = {
            # Español con acentos
            "rol": "Rol",
            "acción": "Acción",
            "aventura": "Aventura",
            "estrategia": "Estrategia",
            "simuladores": "Simuladores",
            "deportes": "Deportes",
            "carreras": "Carreras",
            # Español sin acentos (alternativas para usuarios que no escriben acentos)
            "accion": "Acción",
            "simulador": "Simuladores",
            "deporte": "Deportes",
            "carrera": "Carreras",
            # Inglés
            "rpg": "Rol",
            "action": "Acción",
            "adventure": "Aventura",
            "strategy": "Estrategia",
            "simulation": "Simuladores",
            "simulator": "Simuladores",
            "sports": "Deportes",
            "sport": "Deportes",
            "racing": "Carreras",
            "race": "Carreras",
            "casual": "Casual",
            "indie": "Indie",
            # Multijugador
            "multijugador": "Multijugador masivo",
            "multiplayer": "Multijugador masivo",
            "mmorpg": "Multijugador masivo",
            # Acceso anticipado
            "acceso anticipado": "Acceso anticipado",
            "early access": "Acceso anticipado",
            "beta": "Acceso anticipado",
            # Free to Play
            "free to play": "Free to Play",
            "f2p": "Free to Play",
            "gratis": "Free to Play",
            "gratuito": "Free to Play",
        }
        
        # Detectar intención de búsqueda por género
        # Itera sobre el mapping y busca keywords en la query del usuario
        found_genre = None
        for keyword, genre_name in genre_mapping.items():
            if keyword in query_lower:
                found_genre = genre_name
                break
        
        # Ejecutar búsqueda según intención detectada
        if found_genre:
            # BÚSQUEDA POR GÉNERO: Usuario mencionó un género
            games = game_search.search_by_genre(found_genre, limit=5)
            search_type = f"género {found_genre}"
        else:
            # BÚSQUEDA POR NOMBRE: Procesar como búsqueda de juego específico
            # Estrategia: Extraer palabras significativas, ignorar stopwords comunes
            # Esto mejora la precisión de búsqueda vs. palabras como "el", "un", etc.
            words = request.query.split()
            search_terms = []
            skip_words = {"de", "del", "el", "la", "los", "las", "un", "una", "precio", "cuánto", "cuesta", "vale", "cuál", "es", "qué", "tiene", "dame", "dame", "give", "me", "show", "find", "busca", "búscame", "quiero"}
            for word in words:
                if word.lower() not in skip_words and len(word) > 2:
                    search_terms.append(word)
            
            # Usar los dos primeros términos significativos como búsqueda
            # Ejemplo: "Dame Cyberpunk 2077" → busca "Cyberpunk 2077"
            search_query = " ".join(search_terms[:2]) if search_terms else request.query
            games = game_search.search_by_name(search_query, limit=5)
            search_type = f"búsqueda '{search_query}'"
        
        # 4. FORMATEAR RESPUESTA CONVERSACIONAL
        # Adaptamos la respuesta según cuántos juegos se encontraron
        # para que sea natural y comprensible
        
        if not games:
            # Sin resultados: respuesta amigable con sugerencia
            response_text = f"No encontré juegos para tu consulta: '{request.query}'. Intenta ser más específico o pregunta por otro juego."
            retrieved_games = []
        else:
            # Con resultados: adaptar formato según cantidad
            if len(games) == 1:
                # UN SOLO JUEGO: Mostrar detalles completos
                game = games[0]
                retail = game.get("current_price_retail")
                keyshop = game.get("current_price_keyshop")
                
                # Formatear información de precio de manera amigable
                if retail == 0:
                    price_text = "es GRATIS (free-to-play)"
                elif retail:
                    price_text = f"cuesta {retail:.2f}€ en retail y {keyshop:.2f}€ en keyshops" if keyshop else f"cuesta {retail:.2f}€"
                else:
                    price_text = "no tiene precio disponible en GG.deals"
                
                # Incluir puntuación Metacritic si existe
                metacritic = game.get("metacritic")
                meta_text = f" (Metacritic: {metacritic}/100)" if metacritic else ""
                genres_text = ", ".join(game.get("genres", []))
                
                response_text = f"Encontré '{game.get('name')}'! {price_text}. Es un juego de {genres_text}{meta_text}."
            else:
                # MÚLTIPLES JUEGOS: Listar nombres, usuario puede pedir más detalles
                response_text = f"Encontré {len(games)} juegos para '{search_type}': "
                game_names = []
                for game in games:
                    game_names.append(game.get('name'))
                response_text += ", ".join(game_names) + "."
            
            # Preparar datos para returned_games (información enriquecida)
            # Esta información se incluye en el JSON response para que el cliente
            # pueda mostrar detalles adicionales sin hacer consultas extras
            retrieved_games = []
            for game in games:
                retail = game.get("current_price_retail")
                retrieved_games.append({
                    "name": game.get("name"),
                    "genres": game.get("genres", []),
                    "price": retail if retail else 0,
                    "description": game.get("description", "")[:100]
                })
        
        # 5. Guardar respuesta del asistente
        session_manager.add_message(
            session_id=session_id,
            role="assistant",
            content=response_text
        )
        
        # 6. Retornar respuesta
        session = session_manager.get_session(session_id)
        
        return ChatResponse(
            response=response_text,
            session_id=session_id,
            retrieved_games=retrieved_games,
            message_count=len(session["messages"]),
            timestamp=datetime.now().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Error en /chat: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error procesando consulta: {str(e)}")


@app.post("/chat/reset", tags=["Chat"])
async def reset_chat(session_id: str):
    """
    💬 **RESETEAR CONVERSACIÓN**
    
    Limpia el historial de mensajes de una sesión pero mantiene la sesión activa
    
    Útil para iniciar un nuevo tema de conversación sin perder el ID de sesión
    
    **Ejemplo:**
    ```
    POST /chat/reset?session_id=user_123
    ```
    """
    try:
        session = session_manager.get_session(session_id)
        
        if session is None:
            raise HTTPException(
                status_code=404,
                detail=f"Sesión no encontrada: {session_id}"
            )
        
        session_manager.clear_session(session_id)
        logger.info(f"Sesión reseteada: {session_id}")
        
        return {
            "message": "Conversación reseteada. Puedes iniciar un nuevo tema.",
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en /chat/reset: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chat/history/{session_id}", tags=["Chat"])
async def get_chat_history(session_id: str):
    """
    📜 **OBTENER HISTORIAL DE CONVERSACIÓN**
    
    Devuelve todos los mensajes de una sesión en orden cronológico
    
    **Ejemplo:**
    ```
    GET /chat/history/user_123
    ```
    """
    try:
        history = session_manager.get_chat_history(session_id)
        
        if history is None:
            raise HTTPException(
                status_code=404,
                detail=f"Sesión no encontrada: {session_id}"
            )
        
        return {
            "session_id": session_id,
            "messages": history,
            "message_count": len(history)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en /chat/history: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/chat/stats/{session_id}", response_model=SessionStatsResponse, tags=["Chat"])
async def get_session_stats(session_id: str):
    """
    📊 **ESTADÍSTICAS DE SESIÓN**
    
    Devuelve información sobre una sesión (fecha creación, actividad, conteo mensajes)
    
    **Ejemplo:**
    ```
    GET /chat/stats/user_123
    ```
    """
    try:
        stats = session_manager.get_session_stats(session_id)
        
        if stats is None:
            raise HTTPException(
                status_code=404,
                detail=f"Sesión no encontrada: {session_id}"
            )
        
        return stats
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en /chat/stats: {e}", exc_info=True)
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
