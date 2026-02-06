from sql.sqlite import SQLiteDB
from typing import List, Optional
import sqlite3

class DeveloperDAO:
    """
    Data Access Object (DAO) para la tabla Developer.

    Proporciona métodos para crear, obtener y listar desarrolladores en la base de datos.
    
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
        Crea un nuevo desarrollador en la tabla Developer.

        Args:
            name (str): Nombre del desarrollador.

        Returns:
            int: ID del nuevo desarrollador creado. Retorna -1 si la inserción falla.
        """
        cursor = self.db.execute(
            "INSERT INTO Developer (name) VALUES (?)",
            (name,)
        )
        
        lastId = cursor.lastrowid
        result = -1 if not lastId else lastId
        
        return result
    
    def get(self, dev_id: int) -> Optional[sqlite3.Row]:
        """
        Obtiene un desarrollador por su ID.

        Args:
            dev_id (int): ID del desarrollador.

        Returns:
            Optional[sqlite3.Row]: Fila de la base de datos con los datos del desarrollador,
                                   o None si no existe.
        """
        
        return self.db.fetchone("SELECT * FROM Developer WHERE id = ?", (dev_id,))

    def list_all(self) -> List[sqlite3.Row]:
        """
        Lista todos los desarrolladores de la tabla Developer.

        Returns:
            List[sqlite3.Row]: Lista de filas de la base de datos con todos los desarrolladores.
        """
        
        return self.db.fetchall("SELECT * FROM Developer")
