import requests
from typing import Optional, List
from structures.steam_game import SteamGame, PriceOverview, Genre, Platforms


class SteamAPI:
    """
    Clase que consulta a la API de Steam para obtener datos de videojuegos.
    """

    APP_DETAILS_URL = "https://store.steampowered.com/api/appdetails"  # URL de detalles de un videojuego.
    STORE_SEARCH_URL = "https://store.steampowered.com/api/storesearch" # URL de búsqueda de juegos.


    def __init__(self, api_key: Optional[str] = None, timeout: int = 10):
        """
        Constructor del consultor de la API.

        :param self: self
        :param api_key: API_KEY necesaria para consultar a Steam.
        :type api_key: Optional[str]
        :param timeout: Tiempo de espera por petición.
        :type timeout: int
        """

        self.api_key = api_key              # API_KEY para consultar.
        self.timeout = timeout              # Timeout por si tarde mucho.
        self.session = requests.Session()   # Mantiene la sesión.

    def get_game_by_appid(self, appid: int) -> SteamGame:
        """
        Busca un juego por su AppID.

        :param self: self
        :param appid: ID del videojuego.
        :type appid: int
        :return: Objeto SteamGame con la información del videojuego.
        :rtype: SteamGame
        """

        if appid <= 0:  # En caso de no proporcionar un ID válido.
            raise ValueError("El AppID debe ser un entero positivo")

        # Parámetros para la request.
        params = {
            "appids": appid,    # ID del videojuego.
            "cc": "es",         # Código de país.
            "l": "es"           # Idioma de la información.
        }

        response = self.session.get(
            self.APP_DETAILS_URL,   # URL de los detalles.
            params=params,          # Parámetros del videojuego a buscar.
            timeout=self.timeout    # Tiempo de la consulta.
        )

        response.raise_for_status()  # Suelta una excepción dependiendo del estado devuelto.

        data = response.json()              # Respuesta en JSON.
        app_data = data.get(str(appid))

        if not app_data or not app_data.get("success"):
            raise RuntimeError(f"No se pudo obtener información del AppID {appid}")

        data = app_data["data"]

        # Información del precio (puede no existir si el juego es gratuito).
        price_overview = None
        if "price_overview" in data:
            price_overview = PriceOverview(
                currency=data["price_overview"]["currency"],                    # Divisa.
                initial=data["price_overview"]["initial_formatted"],                      # Precio original.
                final=data["price_overview"]["final_formatted"],                          # Precio con descuento aplicado.
                discount_percent=data["price_overview"]["discount_percent"],    # Procentaje de descuento.
            )

        # Información de plataformas.
        platforms = Platforms(
            windows=data["platforms"]["windows"],
            mac=data["platforms"]["mac"],
            linux=data["platforms"]["linux"],
        )

        # Géneros del videojuego.
        genres = [
            Genre(id=g["id"], description=g["description"])
            for g in data.get("genres", [])
        ]

        return SteamGame(
            appid=data["steam_appid"],                                  # Id
            name=data["name"],                                          # Nombre del videojuego.
            short_description=data.get("short_description", ""),        # Descripción corta.
            developers=data.get("developers", []),                      # Desarrolladores.
            publishers=data.get("publishers", []),                      # Distribuidores.
            price_overview=price_overview,                              # Información del precio.
            platforms=platforms,                                        # Plataformas.
            genres=genres,                                              # Géneros del software.
            is_free=data.get("is_free", False),                         # ¿Es gratuito?
        )

    def search_game_by_name(self, name: str, limit: int = 5) -> List[SteamGame]:
        """
        Busca un juego por su nombre y devuelve objetos SteamGame.
        """
        if not name.strip():
            raise ValueError("El nombre del juego no puede estar vacío")

        params = {"term": name, "l": "spanish", "cc": "ES"}
        response = self.session.get(self.STORE_SEARCH_URL, params=params, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()

        items = data.get("items", [])[:limit]
        games: List[SteamGame] = []

        for item in items:
            try:
                game = self.get_game_by_appid(item["id"])
                games.append(game)
            except Exception as e:
                # Ignora juegos que no se pueden cargar
                print(f"No se pudo cargar {item.get('name')}: {e}")

        return games