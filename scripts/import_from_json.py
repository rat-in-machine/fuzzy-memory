"""
Script rápido para importar games_export.json a MongoDB
Uso: python import_from_json.py games_export.json
"""

import json
import sys
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

def import_games_from_json(json_file: str):
    """Importa juegos desde JSON a MongoDB"""
    
    # Conectar a MongoDB
    mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
    db_name = os.getenv("MONGODB_DB_NAME", "videogames_recommender")
    
    client = MongoClient(mongo_uri)
    db = client[db_name]
    games_collection = db['games']
    
    # Crear índice único en steam_id
    games_collection.create_index('steam_id', unique=True)
    
    print(f"Leyendo {json_file}...")
    
    # Leer JSON
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            games = json.load(f)
    except FileNotFoundError:
        print(f"ERROR: Archivo '{json_file}' no encontrado")
        return
    except json.JSONDecodeError:
        print(f"ERROR: '{json_file}' no es un JSON válido")
        return
    
    print(f"Importando {len(games)} juegos a MongoDB...")
    
    inserted = 0
    duplicated = 0
    errors = 0
    
    for game in games:
        try:
            games_collection.insert_one(game)
            inserted += 1
            print(f"   OK {game.get('name', 'Sin nombre')}")
        except Exception as e:
            if "duplicate key" in str(e).lower():
                duplicated += 1
                print(f"   DUP {game.get('name', 'Sin nombre')} (ya existe)")
            else:
                errors += 1
                print(f"   ERR Error con {game.get('name', 'Sin nombre')}: {e}")
    
    # Estadísticas finales
    total = games_collection.count_documents({})
    with_prices = games_collection.count_documents({"current_price_retail": {"$ne": None}})
    
    print("\n" + "=" * 70)
    print("IMPORTACION COMPLETADA")
    print("=" * 70)
    print(f"\nResultados:")
    print(f"   Insertados: {inserted}")
    print(f"   Duplicados: {duplicated}")
    print(f"   Errores: {errors}")
    print(f"\nEstado de la BD:")
    print(f"   Total juegos: {total}")
    print(f"   Con precios: {with_prices}")
    print(f"   Sin precios: {total - with_prices}")
    
    client.close()
    print("\nListo para usar!")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python import_from_json.py <archivo.json>")
        print("\nEjemplo:")
        print("  python import_from_json.py games_export.json")
        sys.exit(1)
    
    json_file = sys.argv[1]
    import_games_from_json(json_file)
