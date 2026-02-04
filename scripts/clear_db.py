"""Script para limpiar la base de datos MongoDB"""
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv('chatbot/.env')

mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
db_name = os.getenv("MONGODB_DB_NAME", "videogames_recommender")

client = MongoClient(mongo_uri)
db = client[db_name]

# Eliminar todos los documentos de la coleccion games
result = db.games.delete_many({})
print(f"[OK] Eliminados {result.deleted_count} juegos de la base de datos")

client.close()
