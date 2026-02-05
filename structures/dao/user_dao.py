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
            INSERT INTO [User] (name, password, email, role_id)
            VALUES (?, ?, ?, ?);
            SELECT CAST(SCOPE_IDENTITY() AS INT) AS id;
            """,
            (name, password, email, role_id)
        )
        row = cursor.fetchone()
        return row.id if row else -1

    def get(self, user_id: int) -> Optional[pyodbc.Row]:
        """
        Obtiene un usuario por su ID.
        """
        return self.db.fetchone("SELECT id, name, password, email, role_id FROM [User] WHERE id = ?", (user_id,))

    def list_all(self) -> List[pyodbc.Row]:
        """
        Lista todos los usuarios.
        """
        return self.db.fetchall("SELECT id, name, password, email, role_id FROM [User]")

    def get_with_role(self, user_id: int) -> Optional[pyodbc.Row]:
        """
        Obtiene un usuario junto con los datos de su rol y permisos.
        """
        return self.db.fetchone("""
            SELECT u.*, r.name AS role_name, r.can_query, r.can_insert, r.can_update, r.can_delete
            FROM [User] u
            JOIN Role r ON u.role_id = r.id
            WHERE u.id = ?
        """, (user_id,))
