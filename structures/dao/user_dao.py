from typing import List, Optional
import pyodbc
from sql.azure_sqldb import AzureSQLDB  # tu clase de conexión a Azure SQL

class UserDAO:
    """
    DAO para la tabla User en Azure SQL Server.
    """

    def __init__(self, db: AzureSQLDB):
        self.db = db

    def create(self, name: str, password: str, email: str, role_id: int) -> int:
        """
        Crea un nuevo usuario y devuelve su ID.
        """
        cursor = self.db.execute(
            """
            INSERT INTO [Users] (name, password, email, role_id)
            OUTPUT INSERTED.id
            VALUES (?, ?, ?, ?)
            """,
            (name, password, email,     role_id)
        )
        row = cursor.fetchone()
        return row.id if row else -1

    def get(self, user_id: int) -> Optional[pyodbc.Row]:
        """
        Obtiene un usuario por su ID.
        """
        return self.db.fetchone("SELECT id, name, password, email, role_id FROM [Users] WHERE id = ?", (user_id,))

    def list_all(self) -> List[pyodbc.Row]:
        """
        Lista todos los usuarios.
        """
        return self.db.fetchall("SELECT id, name, password, email, role_id FROM [Users]")

    def get_with_role(self, user_id: int) -> Optional[pyodbc.Row]:
        """
        Obtiene un usuario junto con los datos de su rol y permisos.
        """
        return self.db.fetchone("""
            SELECT u.id, u.name, u.password, u.email, r.name AS role_name, r.id, r.can_query, r.can_insert, r.can_update, r.can_delete
            FROM [Users] u
            JOIN Roles r ON u.role_id = r.id
            WHERE u.id = ?
        """, (user_id,))

    def get_by_email(self, email: str) -> Optional[pyodbc.Row]:
        return self.db.fetchone(
            "SELECT id, name, password, email, role_id FROM [Users] WHERE email = ?",
            (email,)
        )
        
    def delete(self, user_id: int) -> bool:
        """
        Elimina un usuario por su ID. Devuelve True si se eliminó un registro.
        """
        cursor = self.db.execute("DELETE FROM [Users] WHERE id = ?", (user_id,))
        return cursor.rowcount > 0