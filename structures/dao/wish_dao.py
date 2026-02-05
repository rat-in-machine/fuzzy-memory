from sql.sqlite import SQLiteDB
from typing import List, Optional
import sqlite3

class WishlistDAO:
    """
    Data Access Object (DAO) para la tabla Wishlist.

    Proporciona métodos para agregar, eliminar y listar juegos en la
    lista de deseos de los usuarios.

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

    def add(self, user_id: int, appid: int) -> None:
        """
        Agrega un juego a la wishlist de un usuario.

        Args:
            user_id (int): ID del usuario.
            appid (int): ID del juego a agregar.
        """
        self.db.execute(
            "INSERT INTO Wishlist (user_id, appid) VALUES (?, ?)",
            (user_id, appid)
        )

    def remove(self, user_id: int, appid: int) -> None:
        """
        Elimina un juego de la wishlist de un usuario.

        Args:
            user_id (int): ID del usuario.
            appid (int): ID del juego a eliminar.
        """
        self.db.execute(
            "DELETE FROM Wishlist WHERE user_id = ? AND appid = ?",
            (user_id, appid)
        )

    def list_by_user(self, user_id: int) -> List[sqlite3.Row]:
        """
        Lista todos los juegos en la wishlist de un usuario, incluyendo el nombre del juego.

        Args:
            user_id (int): ID del usuario.

        Returns:
            List[sqlite3.Row]: Lista de filas con los juegos de la wishlist del usuario,
                               cada fila incluye información de la wishlist y el nombre del juego.
        """
        return self.db.fetchall(
            """
            SELECT w.*, g.name as game_name
            FROM Wishlist w
            JOIN Games g ON w.appid = g.appid
            WHERE w.user_id = ?
            """,
            (user_id,)
        )
