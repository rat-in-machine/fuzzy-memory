from fastapi import APIRouter, HTTPException
from datetime import datetime
import json
import logging
from ..core import ChatRequest, ChatResponse, SessionStatsResponse
from ..session_manager import SessionManager
from src.services.game_search import get_game_search
from src.llm_chatbot.client import LLMStreamingClient
from src.llm_chatbot.prompts import SYSTEM_PROMPT_GAMING_EXPERT

router = APIRouter()
session_manager = SessionManager(session_timeout_minutes=60)
logger = logging.getLogger(__name__)

# Inicializar cliente LLM
llm_client = LLMStreamingClient()

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
    
    # Detectar si se menciona un nombre específico de juego
    # Palabras que indican búsqueda de juego específico
    specific_indicators = ["llama", "llamado", "tal es", "es el", "sobre", "acerca", "que tal", 
                          "dame info", "informacion", "hablame", "cuentame", "ver que tal"]
    is_specific_search = any(indicator in query_lower for indicator in specific_indicators)
    
    # Buscar palabras capitalizadas (probables nombres de juegos)
    words = request.query.split()
    capitalized_words = [w for w in words if w and w[0].isupper() and len(w) > 2 
                         and w.lower() not in ["el", "la", "los", "las", "de", "del"]]
    
    games = []
    search_type = ""
    
    # Prioridad 1: Si hay palabras capitalizadas o indicadores específicos, buscar por nombre exacto
    if capitalized_words or is_specific_search:
        # Usar las palabras capitalizadas o limpiar el query
        if capitalized_words:
            search_query = " ".join(capitalized_words)
        else:
            # Limpiar palabras de búsqueda específica (sin acentos para comparar)
            skip_words = {"de", "del", "el", "la", "los", "las", "un", "una", "precio", "cuanto", 
                         "cuesta", "vale", "cual", "es", "que", "tal", "ver", "dame", "sobre",
                         "acerca", "me", "puedes", "hablame", "cuentame", "informacion"}
            search_terms = [w for w in words if w.lower() not in skip_words and len(w) > 2]
            search_query = " ".join(search_terms[:3]) if search_terms else request.query
        
        games = game_search.search_by_name(search_query, limit=1)  # Buscar solo 1 juego específico
        search_type = f"juego específico '{search_query}'"
        
        # Si no se encontró con nombre específico, intentar búsqueda más amplia
        if not games and search_query != request.query:
            games = game_search.search_by_name(search_query, limit=5)
    
    # Prioridad 2: Buscar por género si no hubo búsqueda específica
    if not games:
        found_genre = None
        for keyword, genre_name in genre_mapping.items():
            if keyword in query_lower:
                found_genre = genre_name
                break
        if found_genre:
            games = game_search.search_by_genre(found_genre, limit=5)
            search_type = f"género {found_genre}"
    
    # Prioridad 3: Búsqueda general por palabras clave
    if not games:
        skip_words = {"de", "del", "el", "la", "los", "las", "un", "una", "precio", "cuanto", "cuesta", "vale", "cual", "es", "que"}
        search_terms = [w for w in words if w.lower() not in skip_words and len(w) > 2]
        search_query = " ".join(search_terms[:2]) if search_terms else request.query
        games = game_search.search_by_name(search_query, limit=5)
        search_type = f"busqueda '{search_query}'"
    
    # Preparar contexto de juegos para el LLM
    if not games:
        game_context = "No se encontraron juegos en la base de datos para esta consulta."
        retrieved_games = []
    else:
        # Construir contexto detallado de juegos
        game_context_parts = []
        for idx, game in enumerate(games, 1):
            retail = game.get("current_price_retail", 0)
            keyshop = game.get("current_price_keyshop", 0)
            
            if retail == 0:
                price_info = "GRATIS (Free-to-Play)"
            elif retail:
                price_info = f"Retail: {retail:.2f}€, Keyshop: {keyshop:.2f}€" if keyshop else f"Precio: {retail:.2f}€"
            else:
                price_info = "Precio no disponible"
            
            metacritic = game.get("metacritic")
            meta_text = f"Metacritic: {metacritic}/100" if metacritic else "Sin puntuación"
            
            game_info = f"""
{idx}. **{game.get('name')}**
   - Géneros: {', '.join(game.get('genres', []))}
   - Precio: {price_info}
   - {meta_text}
   - Descripción: {game.get('description', 'Sin descripción')[:200]}...
"""
            game_context_parts.append(game_info)
        
        game_context = "\n".join(game_context_parts)
        
        # Formatear juegos para respuesta
        retrieved_games = []
        for game in games:
            retail = game.get("current_price_retail")
            keyshop = game.get("current_price_keyshop")
            retrieved_games.append({
                "name": game.get("name"),
                "genres": game.get("genres", []),
                "current_price_retail": retail if retail else 0,
                "current_price_keyshop": keyshop if keyshop else 0,
                "description": game.get("description", ""),
                "metacritic": game.get("metacritic"),
                "header_image": game.get("header_image"),
                "ggdeals_url": game.get("ggdeals_url"),
                "relevance_score": None
            })
    
    # Construir prompt para el LLM
    user_message = f"""Usuario pregunta: "{request.query}"

Juegos relevantes encontrados en nuestra base de datos:
{game_context}

Por favor, responde de manera conversacional y entusiasta. Si encontramos juegos, recomiéndalos explicando por qué son buenas opciones. Si no encontramos juegos, sugiere al usuario que intente con otros términos o géneros."""
    
    # Generar respuesta con LLM
    try:
        logger.info(f"Generando respuesta con LLM para query: {request.query}")
        response_text = llm_client.get_response(
            message=user_message,
            temperature=0.7,
            language="es",
            system_prompt=SYSTEM_PROMPT_GAMING_EXPERT
        )
        logger.info("Respuesta LLM generada exitosamente")
        logger.info(f"Retrieved games antes de buscar mencionados: {len(retrieved_games)}")
        
        # Si no encontramos juegos inicialmente, extraer nombres mencionados en la respuesta del LLM
        if not retrieved_games and response_text:
            import re
            logger.info("Buscando juegos mencionados en la respuesta del LLM...")
            
            # Buscar palabras de 4+ letras que puedan ser nombres de juegos (con o sin mayúscula inicial)
            # Incluir palabras con mayúscula Y palabras que aparezcan entre asteriscos (énfasis markdown)
            potential_games = []
            
            # Patrón 1: Palabras entre asteriscos (énfasis): **Palworld**, *Palworld*
            emphasized = re.findall(r'\*\*?([A-Za-záéíóúñÁÉÍÓÚÑ][A-Za-záéíóúñÁÉÍÓÚÑ\s]{2,}?)\*\*?', response_text)
            potential_games.extend(emphasized)
            
            # Patrón 2: Palabras capitalizadas de 4+ letras
            capitalized = re.findall(r'\b[A-ZÁÉÍÓÚÑ][a-záéíóúñA-ZÁÉÍÓÚÑ]{3,}(?:\s+[A-ZÁÉÍÓÚÑ][a-záéíóúñA-ZÁÉÍÓÚÑ]{2,}){0,2}\b', response_text)
            potential_games.extend(capitalized)
            
            logger.info(f"Palabras potenciales detectadas: {potential_games}")
            
            # Filtrar palabras comunes que no son nombres de juegos
            exclude_words = {"Aquí", "Este", "Estos", "Estas", "Metacritic", "Steam", "Epic", "Aunque", 
                            "También", "Además", "Sin", "Con", "Para", "Por", "Sobre", "Entre", "Desde",
                            "Hasta", "Pero", "Porque", "Cuando", "Donde", "Como", "Muy", "Tiene", "Puedes",
                            "Ofrece", "Incluye", "Permite", "Varios", "Algunos", "Juegos", "Juego"}
            potential_games = [g.strip() for g in potential_games if g.strip() not in exclude_words and len(g.strip()) > 3]
            
            # Eliminar duplicados manteniendo el orden
            seen = set()
            unique_games = []
            for g in potential_games:
                if g.lower() not in seen:
                    seen.add(g.lower())
                    unique_games.append(g)
            
            logger.info(f"Juegos candidatos después de filtrar: {unique_games}")
            
            # Buscar cada juego mencionado en la base de datos
            found_games = []
            for game_name in unique_games[:8]:  # Aumentado a 8 búsquedas
                logger.info(f"Buscando en BD: '{game_name}'")
                search_results = game_search.search_by_name(game_name, limit=1)
                if search_results:
                    logger.info(f"✓ Encontrado: {search_results[0].get('name')}")
                    found_games.extend(search_results)
                else:
                    logger.info(f"✗ No encontrado: '{game_name}'")
            
            # Si encontramos juegos mencionados, agregarlos a retrieved_games
            if found_games:
                logger.info(f"Total de juegos encontrados para mostrar: {len(found_games)}")
                for game in found_games[:3]:  # Máximo 3 juegos mencionados
                    retail = game.get("current_price_retail")
                    keyshop = game.get("current_price_keyshop")
                    retrieved_games.append({
                        "name": game.get("name"),
                        "genres": game.get("genres", []),
                        "current_price_retail": retail if retail else 0,
                        "current_price_keyshop": keyshop if keyshop else 0,
                        "description": game.get("description", ""),
                        "metacritic": game.get("metacritic"),
                        "header_image": game.get("header_image"),
                        "ggdeals_url": game.get("ggdeals_url"),
                        "relevance_score": None
                    })
                logger.info(f"✅ Añadidos {len(retrieved_games)} juegos mencionados: {[g['name'] for g in retrieved_games]}")
            else:
                logger.warning("No se encontraron juegos en la BD que coincidan con los mencionados")
        
    except Exception as e:
        logger.error(f"Error generando respuesta con LLM: {e}")
        # Fallback a respuesta simple si el LLM falla
        if not games:
            response_text = f"No encontré juegos para tu consulta: '{request.query}'. Intenta ser más específico o pregunta por otro juego."
        else:
            game_names = [g.get('name') for g in games]
            response_text = f"Encontré estos juegos para tu búsqueda: {', '.join(game_names)}. ¿Te gustaría saber más sobre alguno?"
    session_manager.add_message(session_id=session_id, role="assistant", content=response_text)
    session = session_manager.get_session(session_id)
    return ChatResponse(
        response=response_text,
        session_id=session_id,
        retrieved_games=retrieved_games,
        message_count=len(session["messages"]),
        timestamp=datetime.now().isoformat()
    )


# ENDPOINT DESHABILITADO: /chat/stream requiere usuario válido registrado en CodingBuddy
# Descomentar cuando se tenga acceso a credenciales válidas

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

@router.get("/games/all", tags=["Games"])
async def get_all_games(page: int = 1, page_size: int = 25):
    """
    Obtiene todos los juegos con paginación
    
    Args:
        page: Número de página (empieza en 1)
        page_size: Cantidad de juegos por página (default: 25)
    """
    game_search = get_game_search()
    result = game_search.get_all_games(page=page, page_size=page_size)
    
    # Formatear juegos para respuesta
    formatted_games = []
    for game in result["games"]:
        retail = game.get("current_price_retail")
        keyshop = game.get("current_price_keyshop")
        formatted_games.append({
            "name": game.get("name"),
            "genres": game.get("genres", []),
            "current_price_retail": retail if retail else 0,
            "current_price_keyshop": keyshop if keyshop else 0,
            "description": game.get("description", ""),
            "metacritic": game.get("metacritic"),
            "header_image": game.get("header_image"),
            "ggdeals_url": game.get("ggdeals_url")
        })
    
    return {
        "games": formatted_games,
        "total": result["total"],
        "page": result["page"],
        "page_size": result["page_size"],
        "total_pages": result["total_pages"]
    }
