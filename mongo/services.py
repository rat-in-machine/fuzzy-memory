from pymongo import MongoClient
from typing import List, Dict, Any

from utils.config import MONGO_DB, MONGO_COLLECTION, MONGO_URI


def serialize_mongo_doc(doc: Dict[str, Any]) -> Dict[str, Any]:
    """
    Convierte un documento de MongoDB en un diccionario JSON-friendly,
    eliminando campos internos no serializables.
    """
    doc = dict(doc)

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

    client = MongoClient(MONGO_URI)
    collection = client[MONGO_DB][MONGO_COLLECTION]

    cursor = collection.find({}).limit(limit)

    games = [serialize_mongo_doc(doc) for doc in cursor]

    client.close()

    return games
