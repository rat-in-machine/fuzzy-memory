from fastapi import APIRouter
import logging

from fastapi import APIRouter, HTTPException
from chat.models import ChatRequest, ChatResponse
from chat.service import chatbot_chain

from fastapi.responses import StreamingResponse
from typing import AsyncGenerator

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse)
async def chat(request: ChatRequest):

    try:
        answer = chatbot_chain.invoke(request.question)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error procesando la pregunta"
        )

    return ChatResponse(
        answer=answer,
        chat_id=request.chat_id
    )
    
@router.post("/stream")
async def chat_stream(request: ChatRequest):

    async def token_stream() -> AsyncGenerator[str, None]:
        try:
            # stream() funciona con runnables
            async for chunk in chatbot_chain.astream(request.question):
                if isinstance(chunk, str):
                    yield chunk
        except Exception:
            yield "\n[ERROR GENERANDO RESPUESTA]\n"

    return StreamingResponse(
        token_stream(),
        media_type="text/plain"
    )

# ENDPOINT DESHABILITADO: /chat/stream requiere usuario válido registrado en CodingBuddy
# Descomentar cuando se tenga acceso a credenciales válidas

# @router.post("/chat/reset", tags=["Chat"])
# async def reset_chat(session_id: str):
#     session = session_manager.get_session(session_id)
#     if session is None:
#         raise HTTPException(status_code=404, detail=f"Sesión no encontrada: {session_id}")
#     session_manager.clear_session(session_id)
#     return {"message": "Conversación reseteada. Puedes iniciar un nuevo tema.", "session_id": session_id, "timestamp": datetime.now().isoformat()}

# @router.get("/chat/history/{session_id}", tags=["Chat"])
# async def get_chat_history(session_id: str):
#     history = session_manager.get_chat_history(session_id)
#     if history is None:
#         raise HTTPException(status_code=404, detail=f"Sesión no encontrada: {session_id}")
#     return {"session_id": session_id, "messages": history, "message_count": len(history)}

# @router.get("/chat/stats/{session_id}", response_model=SessionStatsResponse, tags=["Chat"])
# async def get_session_stats(session_id: str):
#     stats = session_manager.get_session_stats(session_id)
#     if stats is None:
#         raise HTTPException(status_code=404, detail=f"Sesión no encontrada: {session_id}")
#     return stats

# @router.get("/games/all", tags=["Games"])
# async def get_all_games(page: int = 1, page_size: int = 25):
#     """
#     Obtiene todos los juegos con paginación
    
#     Args:
#         page: Número de página (empieza en 1)
#         page_size: Cantidad de juegos por página (default: 25)
#     """
#     game_search = get_game_search()
#     result = game_search.get_all_games(page=page, page_size=page_size)
    
#     # Formatear juegos para respuesta
#     formatted_games = []
#     for game in result["games"]:
#         retail = game.get("current_price_retail")
#         keyshop = game.get("current_price_keyshop")
#         formatted_games.append({
#             "name": game.get("name"),
#             "genres": game.get("genres", []),
#             "current_price_retail": retail if retail else 0,
#             "current_price_keyshop": keyshop if keyshop else 0,
#             "description": game.get("description", ""),
#             "metacritic": game.get("metacritic"),
#             "header_image": game.get("header_image"),
#             "ggdeals_url": game.get("ggdeals_url")
#         })
    
#     return {
#         "games": formatted_games,
#         "total": result["total"],
#         "page": result["page"],
#         "page_size": result["page_size"],
#         "total_pages": result["total_pages"]
#     }