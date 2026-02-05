from sql.sqlite import SQLiteDB
from typing import List, Optional
import sqlite3

class RoleDAO:
    """
    Data Access Object (DAO) para la tabla Role.

    Proporciona métodos para crear, obtener y listar roles en la base de datos.
    Cada rol define permisos básicos sobre operaciones CRUD (consultar, insertar,
    actualizar y eliminar).

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

    def create(self, name: str, can_select: int = 0, can_insert: int = 0, can_update: int = 0, can_delete: int = 0) -> int:
        """
        Crea un nuevo rol en la tabla Role.

        Args:
            name (str): Nombre del rol.
            can_select (int, optional): Permiso para consultar datos. 0 = no, 1 = sí. Por defecto 0.
            can_insert (int, optional): Permiso para insertar datos. 0 = no, 1 = sí. Por defecto 0.
            can_update (int, optional): Permiso para actualizar datos. 0 = no, 1 = sí. Por defecto 0.
            can_delete (int, optional): Permiso para eliminar datos. 0 = no, 1 = sí. Por defecto 0.

        Returns:
            int: ID del nuevo rol creado. Retorna -1 si la inserción falla.
        """
        cursor = self.db.execute(
            "INSERT INTO Role (name, can_query, can_insert, can_update, can_delete) VALUES (?, ?, ?, ?, ?)",
            (name, can_select, can_insert, can_update, can_delete)
        )
        lastId = cursor.lastrowid
        return -1 if not lastId else lastId

    def get(self, role_id: int) -> Optional[sqlite3.Row]:
        """
        Obtiene un rol por su ID.

        Args:
            role_id (int): ID del rol.

        Returns:
            Optional[sqlite3.Row]: Fila con los datos del rol, o None si no existe.
        """
        return self.db.fetchone("SELECT * FROM Role WHERE id = ?", (role_id,))

    def list_all(self) -> List[sqlite3.Row]:
        """
        Lista todos los roles almacenados en la tabla Role.

        Returns:
            List[sqlite3.Row]: Lista de filas con todos los roles.
        """
        return self.db.fetchall("SELECT * FROM Role")
