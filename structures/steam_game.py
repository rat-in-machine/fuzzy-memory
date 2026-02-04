from dataclasses import dataclass
from typing import List, Optional

@dataclass
class PriceOverview:
    """
    Información del precio del juego. Moneda, descuento, precio inicial y final.
    """
    
    currency: str           # Divisa.
    initial: float          # Precio 
    final: float            # Precio final del juego.
    discount_percent: int   # Porcentaje de descuento.

@dataclass
class Platforms:
    """
    Información de las plataformas del juego.
    """
    
    windows: bool           # Compatible con Windows?
    mac: bool               # Compatible con Mac?
    linux: bool             # Compatible con Linux?

@dataclass
class Genre:
    """
    Genero del juego y descripción.
    """
    
    id: str                 # Id.
    description: str        # Descripción.

@dataclass
class SteamGame:
    """
    Estructura de datos compuesta de la información del videojuego.
    """
    
    appid: int                                  # Id
    name: str                                   # Nombre del videojuego.
    short_description: str                      # Descripción corta.
    developers: List[str]                       # Desarrolladores.
    publishers: List[str]                       # Distribuidores.
    price_overview: Optional[PriceOverview]     # Información del precio.
    platforms: Platforms                        # Plataformas disponibles.
    genres: List[Genre]                         # Generos.
    is_free: bool                               # ¿Es gratuito?
