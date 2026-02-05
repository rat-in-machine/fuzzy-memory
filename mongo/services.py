from pymongo import MongoClient
from typing import List, Dict, Any

from utils.config import MONGO_DB, MONGO_COLLECTION, MONGO_URI


def serialize_mongo_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convierte un documento de MongoDB en un diccionario JSON-friendly,
    eliminando campos internos no serializables.
    """
    try:
        doc = dict(doc)
    except Exception as e:
        print("ERROR AL SERIALIZAR EL MONGO: ",e)
    doc.pop("_id", None)

    return doc


def get_games(limit: int = 5) -> List[Dict[str, Any]]:
    """
    Obtiene una lista de documentos de juegos desde MongoDB Atlas.

    :param limit: Número máximo de documentos a recuperar.
    :type limit: int
    :return: Lista de documentos de juegos como diccionarios Python.
    :rtype: list[dict]
    """
    try:
        client = MongoClient(MONGO_URI)
        collection = client[MONGO_DB][MONGO_COLLECTION]

        cursor = collection.find({}).limit(limit)
    except Exception as e:
        print("ERROR AL ACCEDER AL MONGODB PARA OBTENER LOS JUEGOS:", e)


    try:
        games = [serialize_mongo_doc(doc) for doc in cursor]
    finally:
        client.close()

    return games
