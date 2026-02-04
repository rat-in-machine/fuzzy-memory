"""
Cliente para GG.deals API
Documentación: https://gg.deals/api/prices/

IMPORTANTE: GG.deals API usa Steam App IDs, no nombres de juegos.
Endpoint: https://api.gg.deals/v1/prices/by-steam-app-id/?ids=420,730&key=YOUR_KEY
Rate Limits: 100 req/min, 1000/hora
"""

import httpx
import logging
from typing import Optional, Dict, List

logger = logging.getLogger(__name__)


class GGDealsAPIClient:
    """
    Cliente para obtener precios desde GG.deals API
    
    REQUISITOS:
    - API key (obtener en https://gg.deals/settings/)
    - Steam App IDs (no nombres de juegos)
    
    RATE LIMITS:
    - 100 juegos por minuto
    - 1000 juegos por hora
    """
    
    BASE_URL = "https://api.gg.deals/v1"
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.client = httpx.Client(timeout=30.0)
    
    def get_prices_by_steam_ids(self, steam_app_ids: List[int], region: str = "us") -> Dict:
        """
        Obtiene precios de múltiples juegos por Steam App IDs
        
        Args:
            steam_app_ids: Lista de Steam App IDs (máximo 100)
            region: Región para precios (us, eu, gb, etc.) Default: us
            
        Returns:
            Dict con precios indexados por Steam App ID
            
        Ejemplo:
            client.get_prices_by_steam_ids([420, 730])
            # 420 = Half-Life 2, 730 = CS:GO
        """
        if not self.api_key:
            logger.error("API key no configurada")
            return {}
        
        if len(steam_app_ids) > 100:
            logger.warning(f"Limitando a 100 IDs (recibidos {len(steam_app_ids)})")
            steam_app_ids = steam_app_ids[:100]
        
        try:
            url = f"{self.BASE_URL}/prices/by-steam-app-id/"
            params = {
                "ids": ",".join(map(str, steam_app_ids)),
                "key": self.api_key,
                "region": region
            }
            
            response = self.client.get(url, params=params)
            response.raise_for_status()
            
            data = response.json()
            
            if not data.get("success"):
                logger.error(f"API error: {data}")
                return {}
            
            logger.info(f"Precios obtenidos para {len(steam_app_ids)} juegos")
            return data.get("data", {})
            
        except Exception as e:
            logger.error(f"Error obteniendo precios: {e}")
            return {}
    
    def get_game_prices(self, steam_app_id: int, region: str = "us") -> Optional[Dict]:
        """
        Obtiene precios de un solo juego por Steam App ID
        
        Args:
            steam_app_id: Steam App ID del juego
            region: Región para precios (us, eu, gb, etc.)
            
        Returns:
            Dict con información de precios o None si no se encuentra
        """
        prices = self.get_prices_by_steam_ids([steam_app_id], region)
        
        if not prices:
            return None
        
        game_data = prices.get(str(steam_app_id))
        
        if game_data is None:
            logger.warning(f"Juego {steam_app_id} no encontrado en GG.deals")
            return None
        
        return {
            "steam_app_id": steam_app_id,
            "title": game_data.get("title"),
            "url": game_data.get("url"),
            "current_retail": game_data.get("prices", {}).get("currentRetail"),
            "current_keyshops": game_data.get("prices", {}).get("currentKeyshops"),
            "historical_retail": game_data.get("prices", {}).get("historicalRetail"),
            "historical_keyshops": game_data.get("prices", {}).get("historicalKeyshops"),
            "currency": game_data.get("prices", {}).get("currency"),
        }
    
    def get_deals(self, steam_app_ids: List[int], max_price: Optional[float] = None) -> List[Dict]:
        """
        Obtiene ofertas (deals) filtrando por precio máximo
        
        Args:
            steam_app_ids: Lista de Steam App IDs
            max_price: Precio máximo para filtrar
            
        Returns:
            Lista de juegos que cumplen el filtro
        """
        all_prices = self.get_prices_by_steam_ids(steam_app_ids)
        deals = []
        
        for steam_id, game_data in all_prices.items():
            if game_data is None:
                continue
            
            prices = game_data.get("prices", {})
            current_retail = prices.get("currentRetail")
            
            # Filtrar por precio si se especifica
            if max_price and current_retail:
                try:
                    if float(current_retail) > max_price:
                        continue
                except (ValueError, TypeError):
                    continue
            
            deals.append({
                "steam_app_id": int(steam_id),
                "title": game_data.get("title"),
                "url": game_data.get("url"),
                "current_retail": current_retail,
                "current_keyshops": prices.get("currentKeyshops"),
                "currency": prices.get("currency"),
            })
        
        logger.info(f"Encontradas {len(deals)} ofertas")
        return deals
    
    def close(self):
        """Cierra el cliente HTTP"""
        self.client.close()
