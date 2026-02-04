#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test búsqueda directa de nombres de juegos"""

import requests

queries = [
    "elden ring",
    "minecraft",
    "cyberpunk 2077",
    "stardew",
]

print("=" * 80)
print("BÚSQUEDA DIRECTA POR NOMBRE DE JUEGO")
print("=" * 80)

for query in queries:
    response = requests.post(
        "http://127.0.0.1:8000/chat",
        json={"query": query, "session_id": f"game_{query}"},
        headers={"Content-Type": "application/json"}
    )
    
    data = response.json()
    games = data['retrieved_games']
    
    print(f"\nBúsqueda: {query}")
    print(f"Resultado: {data['response']}")
    if games:
        for game in games:
            print(f"  ✓ {game['name']}: {game['price']}€")
    else:
        print("  ❌ Sin resultados")

print("\n" + "=" * 80)
