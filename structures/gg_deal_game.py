from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class GamePrices:
    """
    Contiene información de precios de un juego obtenida desde GG.deals.
    """
    currentRetail: Optional[str]
    currentKeyshops: Optional[str]
    historicalRetail: Optional[str]
    historicalKeyshops: Optional[str]
    currency: str


@dataclass
class GGDealGame:
    """
    Información de un juego en GG.deals, con precios y URL.
    """
    title: str
    url: str
    prices: GamePrices
