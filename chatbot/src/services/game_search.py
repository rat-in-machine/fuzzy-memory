"""
Servicio de búsqueda de juegos en MongoDB
Proporciona múltiples formas de buscar juegos: por nombre, género o Steam ID
"""
from typing import List, Optional, Dict
from pymongo import MongoClient
import os
from dotenv import load_dotenv
import logging
import unicodedata
import re

logger = logging.getLogger(__name__)

# Cargar configuración desde variables de entorno
load_dotenv()

def normalize_text(text: str) -> str:
    """
    Normaliza texto: quita acentos y convierte a minúsculas.
    Útil para búsquedas que ignoran acentos y mayúsculas.
    
    Args:
        text: Texto a normalizar
        
    Returns:
        Texto sin acentos y en minúsculas
    """
    # Normalizar unicode y quitar acentos
    nfkd = unicodedata.normalize('NFKD', text)
    text_without_accents = ''.join([c for c in nfkd if not unicodedata.combining(c)])
    # Convertir a minúsculas
    return text_without_accents.lower()

class GameSearchService:
    """
    Servicio para buscar juegos en MongoDB.
    Proporciona métodos para búsqueda flexible y formateo de resultados.
    """
    
    def __init__(self):
        """
        Inicializa la conexión a MongoDB.
        
        Usa MONGODB_URI y MONGODB_DB_NAME de variables de entorno.
        Se conecta a la colección 'games' de la base de datos.
        """
        self.mongo_uri = os.getenv("MONGODB_URI", "mongodb://localhost:27017")
        self.db_name = os.getenv("MONGODB_DB_NAME", "videogames_recommender")
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.db_name]
        self.games_collection = self.db['games']
    
    def search_by_name(self, game_name: str, limit: int = 10) -> List[Dict]:
        """
        Busca juegos por nombre (busqueda parcial, case-insensitive, ignora acentos)
        
        Args:
            game_name: Nombre del juego a buscar
            limit: Numero maximo de resultados
            
        Returns:
            Lista de juegos encontrados con sus datos
        """
        try:
            # Normalizar la búsqueda
            normalized_search = normalize_text(game_name)
            # Escapar caracteres especiales de regex
            escaped_search = re.escape(normalized_search)
            
            # Obtener TODOS los juegos y filtrar en Python
            # (más eficiente que normalizar en cada query de Mongo)
            all_games = list(self.games_collection.find(
                {},
                {
                    "name": 1,
                    "steam_id": 1,
                    "description": 1,
                    "genres": 1,
                    "developers": 1,
                    "publishers": 1,
                    "release_date": 1,
                    "metacritic": 1,
                    "current_price_retail": 1,
                    "current_price_keyshop": 1,
                    "currency": 1,
                    "ggdeals_url": 1,
                    "header_image": 1
                }
            ))
            
            # Filtrar juegos cuyo nombre normalizado contenga la búsqueda normalizada
            matching_games = [
                game for game in all_games 
                if normalized_search in normalize_text(game.get('name', ''))
            ]
            
            return matching_games[:limit]
            
        except Exception as e:
            logger.error(f"Error buscando juegos por nombre: {e}")
            return []
    
    def search_by_steam_id(self, steam_id: int) -> Optional[Dict]:
        """
        Busca un juego especifico por Steam ID
        
        Args:
            steam_id: Steam App ID del juego
            
        Returns:
            Diccionario con los datos del juego o None
        """
        try:
            game = self.games_collection.find_one(
                {"steam_id": steam_id},
                {
                    "name": 1,
                    "steam_id": 1,
                    "description": 1,
                    "genres": 1,
                    "developers": 1,
                    "publishers": 1,
                    "release_date": 1,
                    "metacritic": 1,
                    "current_price_retail": 1,
                    "current_price_keyshop": 1,
                    "currency": 1,
                    "ggdeals_url": 1,
                    "header_image": 1
                }
            )
            
            return game
            
        except Exception as e:
            logger.error(f"Error buscando juego por Steam ID: {e}")
            return None
    
    def search_by_genre(self, genre: str, limit: int = 20) -> List[Dict]:
        """
        Busca juegos por genero
        
        Args:
            genre: Genero a buscar
            limit: Numero maximo de resultados
            
        Returns:
            Lista de juegos del genero especificado
        """
        try:
            games = list(self.games_collection.find(
                {"genres": {"$regex": genre, "$options": "i"}},
                {
                    "name": 1,
                    "steam_id": 1,
                    "description": 1,
                    "genres": 1,
                    "current_price_retail": 1,
                    "current_price_keyshop": 1,
                    "currency": 1,
                    "metacritic": 1,
                    "header_image": 1,
                    "ggdeals_url": 1
                }
            ).limit(limit))
            
            return games
            
        except Exception as e:
            logger.error(f"Error buscando juegos por genero: {e}")
            return []
    
    def get_all_games(self, page: int = 1, page_size: int = 25) -> Dict:
        """
        Obtiene todos los juegos con paginación
        
        Args:
            page: Número de página (empieza en 1)
            page_size: Cantidad de juegos por página
            
        Returns:
            Diccionario con 'games' (lista de juegos), 'total' (total de juegos), 
            'page' (página actual), 'total_pages' (total de páginas)
        """
        try:
            # Calcular offset
            skip = (page - 1) * page_size
            
            # Obtener total de juegos
            total_games = self.games_collection.count_documents({})
            
            # Calcular total de páginas
            total_pages = (total_games + page_size - 1) // page_size
            
            # Obtener juegos de la página actual
            games = list(self.games_collection.find(
                {},
                {
                    "name": 1,
                    "steam_id": 1,
                    "description": 1,
                    "genres": 1,
                    "current_price_retail": 1,
                    "current_price_keyshop": 1,
                    "currency": 1,
                    "metacritic": 1,
                    "header_image": 1,
                    "ggdeals_url": 1
                }
            ).skip(skip).limit(page_size))
            
            return {
                "games": games,
                "total": total_games,
                "page": page,
                "page_size": page_size,
                "total_pages": total_pages
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo todos los juegos: {e}")
            return {
                "games": [],
                "total": 0,
                "page": page,
                "page_size": page_size,
                "total_pages": 0
            }
    
    def format_game_info(self, game: Dict) -> str:
        """
        Formatea la información de un juego para mostrar al usuario de forma legible.
        
        Incluye: nombre, descripción, géneros, desarrollador, fecha lanzamiento, 
        Metacritic score, y precios en EUR (retail + keyshop).
        
        Args:
            game: Diccionario con datos del juego desde MongoDB
            
        Returns:
            String formateado con separadores visuales y estructura clara
            
        Ejemplo:
            >>> game = {"name": "Elden Ring", "metacritic": 94, "genres": ["Action", "RPG"]}
            >>> print(service.format_game_info(game))
            ======================================================================
            JUEGO: Elden Ring
            ...
        """
        if not game:
            return "Juego no encontrado"
        
        # Extraer datos principales
        name = game.get("name", "Desconocido")
        steam_id = game.get("steam_id", "N/A")
        description = game.get("description", "Sin descripcion")[:200]  # Primeros 200 caracteres
        genres = ", ".join(game.get("genres", ["No especificado"]))
        developers = ", ".join(game.get("developers", ["Desconocido"]))
        release_date = game.get("release_date", "No especificada")
        metacritic = game.get("metacritic", "N/A")
        
        # Información de precios en EUR
        retail = game.get("current_price_retail")
        keyshop = game.get("current_price_keyshop")
        currency = game.get("currency", "EUR")
        ggdeals_url = game.get("ggdeals_url", "")
        
        # Formatear información de precios de forma amigable
        if retail is None:
            price_info = "[SIN PRECIO] No disponible en GG.deals"
        elif retail == 0:
            price_info = "[FREE-TO-PLAY] Juego gratuito"
        else:
            keyshop_str = f"{keyshop:.2f} {currency}" if keyshop and keyshop > 0 else "No disponible"
            price_info = f"Retail: {retail:.2f} {currency} | Keyshop: {keyshop_str}"
        
        # Construir respuesta formateada con estructura visual clara
        result = f"""
{'='*70}
JUEGO: {name}
Steam ID: {steam_id}
{'='*70}

DESCRIPCION:
{description}...

INFORMACION:
- Generos: {genres}
- Desarrollador: {developers}
- Fecha de lanzamiento: {release_date}
- Puntuacion Metacritic: {metacritic}

PRECIOS (EUR):
{price_info}
"""
        
        if ggdeals_url:
            result += f"\nEnlace GG.deals: {ggdeals_url}"
        
        result += "\n" + "="*70
        
        return result
    
    def close(self):
        """
        Cierra la conexión a MongoDB.
        
        Recomendado llamar al finalizar la aplicación para liberar recursos.
        """
        self.client.close()


# ============================================================================
# INSTANCIA GLOBAL Y PATRÓN LAZY LOADING
# ============================================================================
# Se usa patrón lazy loading (inicialización perezosa) para evitar crear
# la conexión a MongoDB si no es necesaria. Solo se conecta cuando se 
# llama a get_game_search() por primera vez.

_game_search_instance = None

def get_game_search():
    """
    Obtiene la instancia global de GameSearchService (singleton).
    
    Usa lazy loading: la conexión a MongoDB se crea solo cuando se necesita.
    
    Returns:
        GameSearchService: Instancia global del servicio
        
    Ejemplo:
        >>> search_service = get_game_search()
        >>> games = search_service.search_by_name("Elden Ring")
    """
    global _game_search_instance
    if _game_search_instance is None:
        _game_search_instance = GameSearchService()
    return _game_search_instance

# Para compatibilidad, también exponemos como propiedad
game_search = property(lambda self: get_game_search())
