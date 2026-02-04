from dataclasses import dataclass
from typing import Optional

@dataclass
class GamePrices:
    """
    Contiene información de precios de un juego obtenida desde GG.deals.
    """
    currentRetail: Optional[str]        # Precio actual en tiendas retail, como string
    currentKeyshops: Optional[str]      # Precio actual en keyshops, como string
    historicalRetail: Optional[str]     # Precio histórico más bajo en tiendas retail
    historicalKeyshops: Optional[str]   # Precio histórico más bajo en keyshops
    currency: str                        # Código de moneda usado en todos los precios

@dataclass
class GGDealGame:
    """
    Información de un juego en GG.deals, con precios y URL.
    """
    title: str          # Título del juego según GG.deals
    url: str            # URL del juego en GG.deals
    prices: GamePrices  # Objeto con la información de precios del juego
