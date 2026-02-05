from sql.sqlite import SQLiteDB
from typing import List, Optional
import sqlite3

class UserDAO:
    """
    Data Access Object (DAO) para la tabla User.

    Proporciona métodos para crear, obtener y listar usuarios en la base de datos,
    así como para obtener información de un usuario junto con los permisos de su rol.

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

    def create(self, name: str, password: str, email: str, role_id: int) -> int:
        """
        Crea un nuevo usuario en la tabla User.

        Args:
            name (str): Nombre del usuario.
            password (str): Contraseña del usuario.
            email (str): Correo electrónico del usuario (único).
            role_id (int): ID del rol asignado al usuario.

        Returns:
            int: ID del nuevo usuario creado. Retorna -1 si la inserción falla.
        """
        cursor = self.db.execute(
            "INSERT INTO User (name, password, email, role_id) VALUES (?, ?, ?, ?)",
            (name, password, email, role_id)
        )
        lastId = cursor.lastrowid
        return -1 if not lastId else lastId

    def get(self, user_id: int) -> Optional[sqlite3.Row]:
        """
        Obtiene un usuario por su ID.

        Args:
            user_id (int): ID del usuario.

        Returns:
            Optional[sqlite3.Row]: Fila con los datos del usuario, o None si no existe.
        """
        return self.db.fetchone("SELECT * FROM User WHERE id = ?", (user_id,))

    def list_all(self) -> List[sqlite3.Row]:
        """
        Lista todos los usuarios almacenados en la tabla User.

        Returns:
            List[sqlite3.Row]: Lista de filas con todos los usuarios.
        """
        return self.db.fetchall("SELECT * FROM User")

    def get_with_role(self, user_id: int) -> Optional[sqlite3.Row]:
        """
        Obtiene un usuario junto con los detalles de su rol y permisos.

        Args:
            user_id (int): ID del usuario.

        Returns:
            Optional[sqlite3.Row]: Fila con los datos del usuario y los campos del rol:
                                   role_name, can_query, can_insert, can_update, can_delete.
                                   Retorna None si el usuario no existe.
        """
        return self.db.fetchone("""
            SELECT u.*, r.name AS role_name, r.can_query, r.can_insert, r.can_update, r.can_delete
            FROM User u
            JOIN Role r ON u.role_id = r.id
            WHERE u.id = ?
        """, (user_id,))
