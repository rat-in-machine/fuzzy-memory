from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from datetime import datetime
import asyncio
import json
import logging
from config.settings import settings
from ..core import ChatRequest, ChatResponse, SessionStatsResponse
from ..session_manager import SessionManager
from src.services.game_search import get_game_search

router = APIRouter()
session_manager = SessionManager(session_timeout_minutes=60)
logger = logging.getLogger(__name__)

genre_mapping = {
    "rol": "Rol", "rpg": "Rol", "acción": "Acción", "action": "Acción",
    "aventura": "Aventura", "adventure": "Aventura", "estrategia": "Estrategia",
    "strategy": "Estrategia", "simuladores": "Simuladores", "simulation": "Simuladores",
    "deportes": "Deportes", "sports": "Deportes", "carreras": "Carreras", "racing": "Carreras",
    "casual": "Casual", "indie": "Indie", "multijugador": "Multijugador masivo",
    "multiplayer": "Multijugador masivo", "mmorpg": "Multijugador masivo",
    "acceso anticipado": "Acceso anticipado", "early access": "Acceso anticipado",
    "free to play": "Free to Play", "f2p": "Free to Play", "gratis": "Free to Play"
}

@router.post("/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(request: ChatRequest):
    session_id = request.session_id or session_manager.create_session()
    session = session_manager.get_session(session_id)
    if session is None:
        session_id = session_manager.create_session(session_id)
    session_manager.add_message(session_id=session_id, role="user", content=request.query)
    game_search = get_game_search()
    query_lower = request.query.lower()
    found_genre = None
    for keyword, genre_name in genre_mapping.items():
        if keyword in query_lower:
            found_genre = genre_name
            break
    if found_genre:
        games = game_search.search_by_genre(found_genre, limit=5)
        search_type = f"género {found_genre}"
    else:
        words = request.query.split()
        search_terms = []
        skip_words = {"de", "del", "el", "la", "los", "las", "un", "una", "precio", "cuánto", "cuesta", "vale", "cuál", "es", "qué"}
        for word in words:
            if word.lower() not in skip_words and len(word) > 2:
                search_terms.append(word)
        search_query = " ".join(search_terms[:2]) if search_terms else request.query
        games = game_search.search_by_name(search_query, limit=5)
        search_type = f"búsqueda '{search_query}'"
    if not games:
        response_text = f"No encontré juegos para tu consulta: '{request.query}'. Intenta ser más específico o pregunta por otro juego."
        retrieved_games = []
    else:
        if len(games) == 1:
            game = games[0]
            retail = game.get("current_price_retail")
            keyshop = game.get("current_price_keyshop")
            if retail == 0:
                price_text = "es GRATIS (free-to-play)"
            elif retail:
                price_text = f"cuesta {retail:.2f}€ en retail y {keyshop:.2f}€ en keyshops" if keyshop else f"cuesta {retail:.2f}€"
            else:
                price_text = "no tiene precio disponible en GG.deals"
            metacritic = game.get("metacritic")
            meta_text = f" (Metacritic: {metacritic}/100)" if metacritic else ""
            genres_text = ", ".join(game.get("genres", []))
            response_text = f"Encontré '{game.get('name')}'! {price_text}. Es un juego de {genres_text}{meta_text}."
        else:
            response_text = f"Encontré {len(games)} juegos para '{search_type}': "
            game_names = [game.get('name') for game in games]
            response_text += ", ".join(game_names) + "."
        retrieved_games = []
        for game in games:
            retail = game.get("current_price_retail")
            retrieved_games.append({
                "name": game.get("name"),
                "genres": game.get("genres", []),
                "price": retail if retail else 0,
                "description": game.get("description", "")[:100],
                "relevance_score": None
            })
    session_manager.add_message(session_id=session_id, role="assistant", content=response_text)
    session = session_manager.get_session(session_id)
    return ChatResponse(
        response=response_text,
        session_id=session_id,
        retrieved_games=retrieved_games,
        message_count=len(session["messages"]),
        timestamp=datetime.now().isoformat()
    )


@router.post("/chat/stream", tags=["Chat"])
async def chat_stream(request: ChatRequest):
    """
    💬 **CHAT CON STREAMING LLM EN VIVO**
    """
    from src.llm.client import LLMStreamingClient
    from src.llm.prompts import get_system_prompt, PromptMode

    async def generate_stream():
        try:
            logger.info(f"Chat Stream - Consulta: '{request.query}'")

            session_id = request.session_id or session_manager.create_session()
            session = session_manager.get_session(session_id)
            if session is None:
                session_id = session_manager.create_session(session_id)

            session_manager.add_message(
                session_id=session_id,
                role="user",
                content=request.query
            )

            game_search = get_game_search()
            query_lower = request.query.lower()

            found_genre = None
            for keyword, genre_name in genre_mapping.items():
                if keyword in query_lower:
                    found_genre = genre_name
                    break

            if found_genre:
                games = game_search.search_by_genre(found_genre, limit=5)
            else:
                words = request.query.split()
                search_terms = []
                skip_words = {"de", "del", "el", "la", "los", "las", "un", "una", 
                            "precio", "cuánto", "cuesta", "vale", "cuál", "es", "qué"}
                for word in words:
                    if word.lower() not in skip_words and len(word) > 2:
                        search_terms.append(word)
                search_query = " ".join(search_terms[:2]) if search_terms else request.query
                games = game_search.search_by_name(search_query, limit=5)

            context_games = []
            for game in games:
                game_info = f"- {game.get('name')} (Géneros: {', '.join(game.get('genres', []))})"
                retail = game.get("current_price_retail")
                if retail == 0:
                    game_info += " [FREE-TO-PLAY]"
                elif retail:
                    game_info += f" - {retail:.2f}€"
                context_games.append(game_info)

            games_context = "\n".join(context_games) if context_games else "No se encontraron juegos relevantes."

            llm_message = f"""Usuario preguntó: {request.query}

Juegos relevantes de nuestra base de datos:
{games_context}

Basándote en estos juegos, proporciona una recomendación amigable y entusiasta."""

            llm_client = LLMStreamingClient(
                api_endpoint=settings.llm_api_endpoint,
                api_key=settings.llm_api_key,
                model=settings.llm_model
            )

            system_prompt = get_system_prompt(PromptMode.RECOMMENDER)

            full_response = ""
            yield f"data: {json.dumps({'type': 'start', 'games_found': len(games)})}\n\n"

            for chunk in llm_client.stream(
                message=llm_message,
                system_prompt=system_prompt,
                temperature=settings.llm_temperature,
                language="es"
            ):
                full_response += chunk
                yield f"data: {json.dumps({'type': 'content', 'chunk': chunk})}\n\n"
                await asyncio.sleep(0.01)

            session_manager.add_message(
                session_id=session_id,
                role="assistant",
                content=full_response
            )

            yield f"data: {json.dumps({'type': 'done', 'session_id': session_id})}\n\n"
            logger.info(f"Stream completado - Session: {session_id}")

        except Exception as e:
            logger.error(f"Error en /chat/stream: {e}", exc_info=True)
            yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"

    return StreamingResponse(generate_stream(), media_type="text/event-stream")

@router.post("/chat/reset", tags=["Chat"])
async def reset_chat(session_id: str):
    session = session_manager.get_session(session_id)
    if session is None:
        raise HTTPException(status_code=404, detail=f"Sesión no encontrada: {session_id}")
    session_manager.clear_session(session_id)
    return {"message": "Conversación reseteada. Puedes iniciar un nuevo tema.", "session_id": session_id, "timestamp": datetime.now().isoformat()}

@router.get("/chat/history/{session_id}", tags=["Chat"])
async def get_chat_history(session_id: str):
    history = session_manager.get_chat_history(session_id)
    if history is None:
        raise HTTPException(status_code=404, detail=f"Sesión no encontrada: {session_id}")
    return {"session_id": session_id, "messages": history, "message_count": len(history)}

@router.get("/chat/stats/{session_id}", response_model=SessionStatsResponse, tags=["Chat"])
async def get_session_stats(session_id: str):
    stats = session_manager.get_session_stats(session_id)
    if stats is None:
        raise HTTPException(status_code=404, detail=f"Sesión no encontrada: {session_id}")
    return stats
