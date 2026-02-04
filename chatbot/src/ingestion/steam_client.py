"""
Cliente para Steam Web API
Documentación: https://steamcommunity.com/dev
"""

import httpx
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)


class SteamAPIClient:
    """
    Cliente para obtener información de videojuegos desde Steam API
    
    Endpoints principales:
    - GetAppList: Lista de todos los juegos
    - GetAppDetails: Detalles de un juego específico
    """
    
    BASE_URL = "https://api.steampowered.com"
    STORE_URL = "https://store.steampowered.com/api"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.client = httpx.Client(timeout=30.0)
    
    def get_app_list(self) -> List[Dict]:
        """
        Obtiene lista completa de juegos de Steam
        
        Returns:
            Lista de diccionarios con {appid, name}
        """
        try:
            url = f"{self.BASE_URL}/ISteamApps/GetAppList/v2/"
            response = self.client.get(url)
            response.raise_for_status()
            
            data = response.json()
            apps = data.get("applist", {}).get("apps", [])
            
            logger.info(f"Obtenidos {len(apps)} juegos de Steam")
            return apps
            
        except Exception as e:
            logger.error(f"Error obteniendo lista de Steam: {e}")
            return []
    
    def get_app_details(self, app_id: int) -> Optional[Dict]:
        """
        Obtiene detalles de un juego específico
        
        Args:
            app_id: ID del juego en Steam
            
        Returns:
            Diccionario con información completa del juego
        """
        try:
            url = f"{self.STORE_URL}/appdetails"
            params = {"appids": app_id, "l": "spanish"}
            
            response = self.client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            app_data = data.get(str(app_id), {})
            
            if not app_data.get("success"):
                logger.warning(f"Juego {app_id} no disponible")
                return None
            
            game_data = app_data.get("data", {})
            
            # Extraer información relevante
            return {
                "steam_id": app_id,
                "name": game_data.get("name"),
                "type": game_data.get("type"),
                "description": game_data.get("short_description", ""),
                "detailed_description": game_data.get("detailed_description", ""),
                "genres": [g.get("description") for g in game_data.get("genres", [])],
                "categories": [c.get("description") for c in game_data.get("categories", [])],
                "developers": game_data.get("developers", []),
                "publishers": game_data.get("publishers", []),
                "release_date": game_data.get("release_date", {}).get("date"),
                "metacritic": game_data.get("metacritic", {}).get("score"),
                "platforms": game_data.get("platforms", {}),
                "header_image": game_data.get("header_image"),
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo detalles del juego {app_id}: {e}")
            return None
    
    def close(self):
        """Cierra el cliente HTTP"""
        self.client.close()
