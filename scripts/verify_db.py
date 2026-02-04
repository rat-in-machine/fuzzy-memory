"""Script para verificar TODOS los juegos en MongoDB"""
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv('chatbot/.env')

mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
db_name = os.getenv("MONGODB_DB_NAME", "videogames_recommender")

client = MongoClient(mongo_uri)
db = client[db_name]

print("=" * 80)
print("  LISTADO COMPLETO DE JUEGOS EN MONGODB")
print("=" * 80)

# Estadisticas generales
total = db.games.count_documents({})
with_prices = db.games.count_documents({"current_price_retail": {"$ne": None, "$gt": 0}})
free_games = db.games.count_documents({"current_price_retail": 0})
no_price = total - with_prices - free_games

print(f"\n[ESTADISTICAS]")
print(f"   Total juegos: {total}")
print(f"   Con precios: {with_prices}")
print(f"   Free-to-Play: {free_games}")
print(f"   Sin precio: {no_price}")

# Obtener TODOS los juegos ordenados por nombre
all_games = db.games.find(
    {},
    {"name": 1, "current_price_retail": 1, "current_price_keyshop": 1, "currency": 1, "steam_id": 1}
).sort("name", 1)

print(f"\n{'=' * 80}")
print(f"  TODOS LOS JUEGOS ({total} total)")
print(f"{'=' * 80}\n")

count = 0
for game in all_games:
    count += 1
    name = game.get('name', 'Unknown')
    retail = game.get("current_price_retail")
    keyshop = game.get("current_price_keyshop")
    currency = game.get("currency", "EUR")
    
    # Formatear salida segun tipo de juego
    if retail is None:
        # Sin precio disponible
        print(f"{count:3}. {name}")
        print(f"     [SIN PRECIO] No disponible en GG.deals")
    elif retail == 0:
        # Free-to-Play
        print(f"{count:3}. {name}")
        print(f"     [FREE-TO-PLAY] Juego gratuito")
    else:
        # Con precio
        print(f"{count:3}. {name}")
        if keyshop and keyshop > 0:
            print(f"     Retail: {retail:.2f} {currency} | Keyshop: {keyshop:.2f} {currency}")
        else:
            print(f"     Retail: {retail:.2f} {currency} | Keyshop: No disponible")
    
    print()  # Linea en blanco entre juegos

# Resumen final
print("=" * 80)
print(f"[RESUMEN] Mostrando {count} de {total} juegos")
print(f"   - {with_prices} juegos con precio")
print(f"   - {free_games} juegos Free-to-Play")
print(f"   - {no_price} juegos sin precio")
print("=" * 80)

client.close()
