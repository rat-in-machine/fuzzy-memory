from sql.sqlite import SQLiteDB
from typing import List, Optional
import sqlite3

class GameDAO:
    """
    Data Access Object (DAO) para la tabla Games.

    Proporciona métodos para crear, obtener, listar y eliminar juegos
    en la base de datos.

    Attributes:
        db (SQLiteDB): Instancia de la base de datos SQLite para ejecutar consultas.
    """
    
    def __init__(self, db: SQLiteDB):
        """
        Inicializa el DAO con la instancia de la base de datos.

        Args:
            db (SQLiteDB): Conexión a la base de datos SQLite.
        """
        self.db = db

    def create(self, appid: int, name: str, short_description: str,
               currency: Optional[str], initial_price: Optional[float],
               final_price: Optional[float], discount_percent: Optional[int],
               is_free: bool,
               windows: bool, mac: bool, linux: bool) -> None:
        """
        Crea un nuevo registro de juego en la tabla Games.

        Args:
            appid (int): Identificador único del juego.
            name (str): Nombre del juego.
            short_description (str): Descripción breve del juego.
            currency (Optional[str]): Moneda del precio del juego (ej. 'USD').
            initial_price (Optional[float]): Precio original del juego.
            final_price (Optional[float]): Precio final con descuento.
            discount_percent (Optional[int]): Porcentaje de descuento aplicado.
            is_free (bool): Indica si el juego es gratuito.
            windows (bool): Indica disponibilidad en Windows.
            mac (bool): Indica disponibilidad en macOS.
            linux (bool): Indica disponibilidad en Linux.
        """
        
        self.db.execute(
            """
            INSERT INTO Games
            (appid, name, short_description, currency, initial_price,
             final_price, discount_percent, is_free, windows, mac, linux)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (appid, name, short_description, currency, initial_price,
             final_price, discount_percent, int(is_free),
             int(windows), int(mac), int(linux))
        )

    def get(self, appid: int) -> Optional[sqlite3.Row]:
        """
        Obtiene un juego por su appid.

        Args:
            appid (int): Identificador único del juego.

        Returns:
            Optional[sqlite3.Row]: Fila con los datos del juego, o None si no existe.
        """
        
        return self.db.fetchone("SELECT * FROM Games WHERE appid = ?", (appid,))

    def list_all(self) -> List[sqlite3.Row]:
        """
        Lista todos los juegos almacenados en la tabla Games.

        Returns:
            List[sqlite3.Row]: Lista de filas con todos los juegos.
        """
        
        return self.db.fetchall("SELECT * FROM Games")

    def delete(self, appid: int) -> None:
        """
        Elimina un juego de la tabla Games según su appid.

        Args:
            appid (int): Identificador único del juego a eliminar.
        """
        self.db.execute("DELETE FROM Games WHERE appid = ?", (appid,))
