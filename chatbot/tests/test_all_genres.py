#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test de TODOS los géneros disponibles"""

import requests

# Todos los géneros disponibles en BD
genres_to_test = [
    ("Rol", "RPG games"),
    ("Acción", "action games"),
    ("Aventura", "adventure games"),
    ("Estrategia", "strategy games"),
    ("Simuladores", "simulation games"),
    ("Deportes", "sports games"),
    ("Carreras", "racing games"),
    ("Casual", "casual games"),
    ("Indie", "indie games"),
    ("Multijugador masivo", "multiplayer games"),
    ("Acceso anticipado", "early access games"),
    ("Free to Play", "f2p games"),
]

print("=" * 80)
print("PRUEBA DE TODOS LOS GÉNEROS DISPONIBLES")
print("=" * 80)

for genre_es, genre_en in genres_to_test:
    # Alternar entre español e inglés
    query = f"dame juegos de {genre_es.lower()}" if len(genre_es) < 15 else f"give me {genre_en}"
    
    try:
        response = requests.post(
            "http://127.0.0.1:8000/chat",
            json={"query": query, "session_id": f"test_{genre_es}"},
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        data = response.json()
        games = data['retrieved_games']
        
        # Verificar que encontró juegos
        if games:
            print(f"\n✓ {genre_es.upper()}")
            print(f"  Query: '{query}'")
            print(f"  Encontrados: {len(games)} juegos")
            for i, game in enumerate(games[:3], 1):  # Mostrar primeros 3
                print(f"    {i}. {game['name']} ({game['price']}€) - {', '.join(game['genres'])}")
            if len(games) > 3:
                print(f"    ... y {len(games)-3} más")
        else:
            print(f"\n✗ {genre_es.upper()} - NO ENCONTRÓ JUEGOS")
            print(f"  Query: '{query}'")
            print(f"  Respuesta: {data['response']}")
            
    except Exception as e:
        print(f"\n✗ {genre_es.upper()} - ERROR")
        print(f"  Error: {str(e)}")

print("\n" + "=" * 80)
print("PRUEBA COMPLETADA")
print("=" * 80)
