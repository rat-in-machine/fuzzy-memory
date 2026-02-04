"""
Cliente para GG.deals API
Documentación: https://gg.deals/api/
"""

import httpx
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)


class GGDealsAPIClient:
    """
    Cliente para obtener precios e información de ofertas desde GG.deals
    
    Nota: GG.deals API tiene límites de rate. Los datos se cachean localmente.
    """
    
    BASE_URL = "https://api.gg.deals/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {api_key}"} if api_key else {}
        self.client = httpx.Client(timeout=30.0, headers=self.headers)
    
    def search_game(self, game_name: str) -> List[Dict]:
        """
        Busca un juego por nombre
        
        Args:
            game_name: Nombre del juego a buscar
            
        Returns:
            Lista de resultados con precios
        """
        try:
            url = f"{self.BASE_URL}/games/search"
            params = {"title": game_name}
            
            response = self.client.get(url, params=params)
            response.raise_for_status()
            
            results = response.json()
            logger.info(f"Encontrados {len(results)} resultados para '{game_name}'")
            return results
            
        except Exception as e:
            logger.error(f"Error buscando juego '{game_name}': {e}")
            return []
    
    def get_game_prices(self, game_id: str) -> Optional[Dict]:
        """
        Obtiene precios actuales e históricos de un juego
        
        Args:
            game_id: ID del juego en GG.deals
            
        Returns:
            Diccionario con información de precios
        """
        try:
            url = f"{self.BASE_URL}/games/{game_id}/prices"
            
            response = self.client.get(url)
            response.raise_for_status()
            
            price_data = response.json()
            
            return {
                "game_id": game_id,
                "current_price": price_data.get("current_lowest", {}).get("price"),
                "currency": price_data.get("current_lowest", {}).get("currency"),
                "store": price_data.get("current_lowest", {}).get("store"),
                "historical_low": price_data.get("historical_low", {}).get("price"),
                "prices_history": price_data.get("history", []),
                "is_retail": price_data.get("current_lowest", {}).get("is_retail", False),
            }
            
        except Exception as e:
            logger.error(f"Error obteniendo precios del juego {game_id}: {e}")
            return None
    
    def get_deals(self, limit: int = 50) -> List[Dict]:
        """
        Obtiene las mejores ofertas actuales
        
        Args:
            limit: Número máximo de ofertas a obtener
            
        Returns:
            Lista de ofertas
        """
        try:
            url = f"{self.BASE_URL}/deals"
            params = {"limit": limit}
            
            response = self.client.get(url, params=params)
            response.raise_for_status()
            
            deals = response.json()
            logger.info(f"Obtenidas {len(deals)} ofertas")
            return deals
            
        except Exception as e:
            logger.error(f"Error obteniendo ofertas: {e}")
            return []
    
    def close(self):
        """Cierra el cliente HTTP"""
        self.client.close()
