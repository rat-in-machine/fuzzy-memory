#!/usr/bin/env python
"""Exporta todos los juegos de MongoDB a un archivo JSON"""

from pymongo import MongoClient
import json
import os
from dotenv import load_dotenv

load_dotenv()

# Conectar a MongoDB
client = MongoClient(os.getenv("MONGODB_URI", "mongodb://localhost:27017"))
db = client["videogames_recommender"]
games_collection = db["games"]

# Obtener todos los juegos
games = list(games_collection.find({}, {"_id": 0}))

print(f"[OK] Exportando {len(games)} juegos...")

# Guardar a JSON
with open("games_export.json", "w", encoding="utf-8") as f:
    json.dump(games, f, ensure_ascii=False, indent=2)

print(f"[OK] Juegos exportados a: games_export.json")
print(f"[OK] Total: {len(games)} juegos")

# Estadísticas
with_price = sum(1 for g in games if g.get("current_price_retail") and g.get("current_price_retail") > 0)
free = sum(1 for g in games if g.get("current_price_retail") == 0)
no_price = sum(1 for g in games if g.get("current_price_retail") is None)

print(f"\n[STATS]")
print(f"  - Con precio: {with_price}")
print(f"  - Gratuitos (F2P): {free}")
print(f"  - Sin precio: {no_price}")
