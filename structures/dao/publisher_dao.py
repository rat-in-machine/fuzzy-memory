from sql.sqlite import SQLiteDB
from typing import List, Optional
import sqlite3

class PublisherDAO:
    """
    Data Access Object (DAO) para la tabla Publisher.

    Proporciona métodos para crear, obtener y listar editoras en la base de datos.

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

    def create(self, name: str) -> int:
        """
        Crea una nueva editora en la tabla Publisher.

        Args:
            name (str): Nombre de la editora.

        Returns:
            int: ID del nuevo registro creado. Retorna -1 si la inserción falla.
        """
        cursor = self.db.execute(
            "INSERT INTO Publisher (name) VALUES (?)",
            (name,)
        )
        
        lastId = cursor.lastrowid
        result = -1 if not lastId else lastId
        
        return result
    
    def get(self, pub_id: int) -> Optional[sqlite3.Row]:
        """
        Obtiene una editora por su ID.

        Args:
            pub_id (int): ID de la editora.

        Returns:
            Optional[sqlite3.Row]: Fila con los datos de la editora, o None si no existe.
        """
        return self.db.fetchone("SELECT * FROM Publisher WHERE id = ?", (pub_id,))

    def list_all(self) -> List[sqlite3.Row]:
        """
        Lista todas las editoras almacenadas en la tabla Publisher.

        Returns:
            List[sqlite3.Row]: Lista de filas con todas las editoras.
        """
        return self.db.fetchall("SELECT * FROM Publisher")
