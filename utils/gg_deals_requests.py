import requests
from typing import List, Dict, Optional
from dataclasses import dataclass
from decimal import Decimal
from structures.gg_deal_game import GamePrices, GGDealGame


class GGDealsPricesAPI:
    """
    Clase que consulta la API de precios de GG.deals por Steam AppID.
    """

    BASE_URL = "https://api.gg.deals/v1/prices/by-steam-app-id/"

    def __init__(self, api_key: str, timeout: int = 10):
        """
        Constructor de la API de GG.deals.

        :param api_key: Clave única de usuario generada en GG.deals.
        :param timeout: Tiempo de espera por petición.
        """
        self.api_key = api_key
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0"
        })

    def get_prices_by_appids(
        self,
        appids: List[int],
        region: str = "us"
    ) -> Dict[int, Optional['GGDealGame']]:
        """
        Obtiene información de precios de una lista de Steam App IDs.

        :param appids: Lista de Steam App IDs (máximo 100).
        :param region: Región para obtener precios (por defecto 'us').
        :return: Diccionario de AppID -> GGDealGame o None si no se encuentra.
        """
        if not appids:
            raise ValueError("Debe proporcionar al menos un AppID")

        if len(appids) > 100:
            raise ValueError("Se pueden consultar un máximo de 100 AppIDs por solicitud")

        params = {
            "key": self.api_key,
            "ids": ",".join(str(a) for a in appids),
            "region": region
        }

        response = self.session.get(
            self.BASE_URL,
            params=params,
            timeout=self.timeout
        )
        response.raise_for_status()
        data = response.json()

        if not data.get("success", False):
            raise RuntimeError(f"Error al consultar GG.deals: {data.get('data')}")

        result: Dict[int, Optional[GGDealGame]] = {}
        for appid_str, game_data in data.get("data", {}).items():
            appid_int = int(appid_str)
            if game_data is None:
                result[appid_int] = None
                continue

            prices_data = game_data.get("prices", {})
            prices = GamePrices(
                currentRetail=prices_data.get("currentRetail"),
                currentKeyshops=prices_data.get("currentKeyshops"),
                historicalRetail=prices_data.get("historicalRetail"),
                historicalKeyshops=prices_data.get("historicalKeyshops"),
                currency=prices_data.get("currency", "USD")
            )

            result[appid_int] = GGDealGame(
                title=game_data["title"],
                url=game_data["url"],
                prices=prices
            )

        return result
