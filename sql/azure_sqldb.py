from typing import Any, Iterable, Optional, List
import pyodbc 


class AzureSQLDB:
    """
    Gestor ligero de base de datos Azure SQL basado en pyodbc.
    Encapsula conexión, ejecución de consultas y manejo de transacciones.
    """

    def __init__(self, server: str, database: str, username: str, password: str, driver: str = '{ODBC Driver 18 for SQL Server}'):
        """
        Inicializa el gestor con los datos de conexión.

        :param server: Nombre del servidor de Azure SQL (e.g., 'mi-servidor.database.windows.net')
        :param database: Nombre de la base de datos
        :param username: Usuario
        :param password: Contraseña
        :param driver: Driver ODBC a usar
        """
        self.server = server
        self.database = database
        self.username = username
        self.password = password
        self.driver = driver
        self.conn: Optional[pyodbc.Connection] = None

    # -------------------------
    # Context manager
    # -------------------------

    def __enter__(self) -> "AzureSQLDB":
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        if self.conn:
            if exc_type is not None:
                self.conn.rollback()
            else:
                self.conn.commit()
            self.close()

    # -------------------------
    # Conexión
    # -------------------------

    def connect(self) -> None:
        if self.conn is None:
            conn_str = (
                f"DRIVER={self.driver};"
                f"SERVER={self.server};"
                f"DATABASE={self.database};"
                f"UID={self.username};"
                f"PWD={self.password};"
                f"Encrypt=yes;"
                f"TrustServerCertificate=no;"
                f"Connection Timeout=30;"
            )
            self.conn = pyodbc.connect(conn_str)
    
    def close(self) -> None:
        if self.conn:
            self.conn.close()
            self.conn = None

    # -------------------------
    # Ejecución SQL
    # -------------------------

    def execute(self, query: str, params: Iterable[Any] = ()) -> pyodbc.Cursor:
        if self.conn is None:
            raise RuntimeError("La base de datos no está conectada")
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        return cursor

    def executemany(self, query: str, params_list: List[Any]) -> pyodbc.Cursor:
        if self.conn is None:
            raise RuntimeError("La base de datos no está conectada")
        cursor = self.conn.cursor()
        cursor.executemany(query, params_list)
        return cursor

    def executescript(self, script: str) -> None:
        """
        pyodbc no soporta executescript como SQLite.
        Para scripts largos, se recomienda separar queries por ';' y ejecutar en loop.
        """
        if self.conn is None:
            raise RuntimeError("La base de datos no está conectada")
        
        cursor = self.conn.cursor()
        for statement in script.split(';'):
            stmt = statement.strip()
            if stmt:
                cursor.execute(stmt)
        cursor.commit()

    # -------------------------
    # Lectura
    # -------------------------

    def fetchone(self, query: str, params: Iterable[Any] = ()) -> Optional[pyodbc.Row]:
        cursor = self.execute(query, params)
        return cursor.fetchone()

    def fetchall(self, query: str, params: Iterable[Any] = ()) -> list[pyodbc.Row]:
        cursor = self.execute(query, params)
        return cursor.fetchall()
