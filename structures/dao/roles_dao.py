from typing import List, Optional
import pyodbc
from sql.azure_sqldb import AzureSQLDB  # tu clase de conexión a Azure SQL

class RoleDAO:
    """
    DAO para la tabla Role en Azure SQL Server.
    """

    def __init__(self, db: AzureSQLDB):
        """
        Inicializa el DAO con la instancia de la base de datos.
        """
        self.db = db

    def create(self, name: str, can_select: int = 0, can_insert: int = 0,
               can_update: int = 0, can_delete: int = 0) -> int:
        """
        Crea un nuevo rol y devuelve su ID.
        """
        cursor = self.db.execute(
            """
            INSERT INTO Role (name, can_query, can_insert, can_update, can_delete)
            VALUES (?, ?, ?, ?, ?);
            SELECT CAST(SCOPE_IDENTITY() AS INT) AS id;
            """,
            (name, can_select, can_insert, can_update, can_delete)
        )
        row = cursor.fetchone()
        return row.id if row else -1

    def get(self, role_id: int) -> Optional[pyodbc.Row]:
        """
        Obtiene un rol por su ID.
        """
        return self.db.fetchone("SELECT id, name, can_query, can_update, can_delete, can_insert FROM Role WHERE id = ?", (role_id,))

    def list_all(self) -> List[pyodbc.Row]:
        """
        Lista todos los roles.
        """
        return self.db.fetchall("SELECT id, name, can_query, can_update, can_delete, can_insert FROM Role")
