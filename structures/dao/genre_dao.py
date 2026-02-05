from sql.sqlite import SQLiteDB
from typing import List, Optional
import sqlite3

class GenreDAO:
    """
    Data Access Object (DAO) para la tabla Genre.

    Proporciona métodos para crear, obtener y listar géneros en la base de datos.

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

    def create(self, genre_id: str, description: str) -> None:
        """
        Crea un nuevo género en la tabla Genre.

        Args:
            genre_id (str): Identificador único del género.
            description (str): Descripción del género.
        """
        self.db.execute(
            "INSERT INTO Genre (id, description) VALUES (?, ?)",
            (genre_id, description)
        )

    def get(self, genre_id: str) -> Optional[sqlite3.Row]:
        """
        Obtiene un género por su ID.

        Args:
            genre_id (str): Identificador único del género.

        Returns:
            Optional[sqlite3.Row]: Fila con los datos del género, o None si no existe.
        """
        return self.db.fetchone("SELECT * FROM Genre WHERE id = ?", (genre_id,))

    def list_all(self) -> List[sqlite3.Row]:
        """
        Lista todos los géneros almacenados en la tabla Genre.

        Returns:
            List[sqlite3.Row]: Lista de filas con todos los géneros.
        """
        return self.db.fetchall("SELECT * FROM Genre")
