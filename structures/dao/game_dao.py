from typing import List, Optional
import pyodbc
from sql.azure_sqldb import AzureSQLDB 

class GameDAO:
    """
    Data Access Object (DAO) para la tabla Games en Azure SQL Server.
    """

    def __init__(self, db: AzureSQLDB):
        """
        Inicializa el DAO con la instancia de la base de datos.

        Args:
            db (AzureSQLDB): Conexión a Azure SQL Server.
        """
        self.db = db

    def create(self, appid: int, name: str, short_description: str,
               currency: Optional[str], initial_price: Optional[float],
               final_price: Optional[float], discount_percent: Optional[int],
               is_free: bool,
               windows: bool, mac: bool, linux: bool) -> None:
        """
        Crea un nuevo registro de juego.
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

    def get(self, appid: int) -> Optional[pyodbc.Row]:
        """
        Obtiene un juego por su appid.
        """
        return self.db.fetchone("SELECT * FROM Games WHERE appid = ?", (appid,))

    def list_all(self) -> List[pyodbc.Row]:
        """
        Lista todos los juegos.
        """
        return self.db.fetchall("SELECT appid, name, short_description, is_free FROM Games")

    def delete(self, appid: int) -> None:
        """
        Elimina un juego según su appid.
        """
        self.db.execute("DELETE FROM Games WHERE appid = ?", (appid,))
