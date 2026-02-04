#!/usr/bin/env python
"""
Script de diagnóstico para el endpoint /chat
"""
import sys
import traceback
import json

try:
    from src.api.main import app, ChatRequest, ChatResponse, session_manager, get_game_search
    print("✓ FastAPI app imports successful")
    
    # Simular una petición POST al endpoint /chat
    request = ChatRequest(
        query="Recomiendame un juego de rol",
        session_id="test_session_001"
    )
    print(f"✓ ChatRequest created: {request.query}")
    
    # Intentar ejecutar la lógica del endpoint
    print("\nExecuting chat endpoint logic...")
    
    # 1. Gestión de sesión
    session_id = request.session_id or session_manager.create_session()
    session = session_manager.get_session(session_id)
    if session is None:
        session_id = session_manager.create_session(session_id)
    print(f"✓ Session created/retrieved: {session_id}")
    
    # 2. Guardar mensaje
    session_manager.add_message(session_id=session_id, role="user", content=request.query)
    print(f"✓ User message saved")
    
    # 3. Procesar búsqueda
    game_search = get_game_search()
    query_lower = request.query.lower()
    
    # Detectar géneros
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
    
    found_genre = None
    for keyword, genre_name in genre_mapping.items():
        if keyword in query_lower:
            found_genre = genre_name
            break
    
    print(f"✓ Detected genre: {found_genre}")
    
    if found_genre:
        games = game_search.search_by_genre(found_genre, limit=5)
        search_type = f"género {found_genre}"
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
        search_type = f"búsqueda '{search_query}'"
    
    print(f"✓ Games found: {len(games)}")
    if games:
        print(f"  - First game: {games[0].get('name')}")
    
    # 4. Formatear respuesta
    if not games:
        response_text = f"No encontré juegos para tu consulta: '{request.query}'."
    else:
        if len(games) == 1:
            game = games[0]
            retail = game.get("current_price_retail")
            if retail == 0:
                price_text = "es GRATIS (free-to-play)"
            elif retail:
                keyshop = game.get("current_price_keyshop")
                price_text = f"cuesta {retail:.2f}€ en retail y {keyshop:.2f}€ en keyshops" if keyshop else f"cuesta {retail:.2f}€"
            else:
                price_text = "no tiene precio disponible"
            
            metacritic = game.get("metacritic")
            meta_text = f" (Metacritic: {metacritic}/100)" if metacritic else ""
            genres_text = ", ".join(game.get("genres", []))
            response_text = f"Encontré '{game.get('name')}'! {price_text}. Es un juego de {genres_text}{meta_text}."
        else:
            response_text = f"Encontré {len(games)} juegos para '{search_type}': "
            game_names = [game.get('name') for game in games]
            response_text += ", ".join(game_names) + "."
    
    print(f"✓ Response generated: {response_text[:50]}...")
    
    # 5. Guardar respuesta
    session_manager.add_message(session_id=session_id, role="assistant", content=response_text)
    print(f"✓ Response saved to session")
    
    print("\n✓ All checks passed!")
    
except Exception as e:
    print(f"\n✗ Error: {type(e).__name__}: {e}")
    traceback.print_exc()
    sys.exit(1)
