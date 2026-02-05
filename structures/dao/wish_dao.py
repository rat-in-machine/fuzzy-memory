from typing import List
import pyodbc
from sql.azure_sqldb import AzureSQLDB  # tu clase de conexión a Azure SQL

class WishlistDAO:
    """
    DAO para la tabla Wishlist en Azure SQL Server.
    """

    def __init__(self, db: AzureSQLDB):
        self.db = db

    def add(self, user_id: int, appid: int) -> None:
        """
        Agrega un juego a la wishlist de un usuario.
        """
        self.db.execute(
            "INSERT INTO Wishlist (user_id, appid) VALUES (?, ?)",
            (user_id, appid)
        )

    def remove(self, user_id: int, appid: int) -> None:
        """
        Elimina un juego de la wishlist de un usuario.
        """
        self.db.execute(
            "DELETE FROM Wishlist WHERE user_id = ? AND appid = ?",
            (user_id, appid)
        )

    def list_by_user(self, user_id: int) -> List[pyodbc.Row]:
        """
        Lista todos los juegos en la wishlist de un usuario, incluyendo el nombre del juego.
        """
        return self.db.fetchall(
            """
            SELECT w.id, w.user_id, w.appid, g.name AS game_name
            FROM Wishlist w
            JOIN Games g ON w.appid = g.appid
            WHERE w.user_id = ?
            """,
            (user_id,)
        )
