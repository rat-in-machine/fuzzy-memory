import sqlite3
from typing import Any, Iterable, Optional


class SQLiteDB:
    """
    Gestor ligero de base de datos SQLite basado en sqlite3 (DB-API 2.0).
    Encapsula conexión, ejecución de consultas y manejo de transacciones.
    """

    def __init__(self, db_path: str):
        """
        Inicializa el gestor con la ruta de la base de datos.

        :param db_path: Ruta al archivo SQLite (.db)
        """
        self.db_path = db_path
        self.conn: Optional[sqlite3.Connection] = None

    # -------------------------
    # Context manager
    # -------------------------

    def __enter__(self) -> "SQLiteDB":
        """
        Abre la conexión al entrar en un bloque with.
        """
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        """
        Cierra la conexión al salir del bloque with.
        Si ocurrió una excepción, revierte la transacción.
        """
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
            # Permitir usar la misma conexión en distintos hilos
            self.conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self.conn.row_factory = sqlite3.Row
            self.conn.execute("PRAGMA foreign_keys = ON")

    def close(self) -> None:
        """
        Cierra la conexión activa.
        """
        if self.conn:
            self.conn.close()
            self.conn = None

    # -------------------------
    # Ejecución SQL
    # -------------------------

    def execute(self, query: str, params = ()) -> sqlite3.Cursor:
        if self.conn is None:
            raise RuntimeError("La base de datos no está conectada")
        
        cursor = self.conn.cursor()
        cursor.execute(query, params) 
        return cursor

    def executemany(self, query: str, params_list = ()) -> sqlite3.Cursor:
        
        if self.conn is None:
            raise RuntimeError("La base de datos no está conectada")
        cursor = self.conn.cursor()
        cursor.executemany(query, params_list) 
        return cursor


    def executescript(self, script: str) -> None:
        """
        Ejecuta un script SQL completo.

        :param script: Script SQL.
        """
        if self.conn is None:
            raise RuntimeError("La base de datos no está conectada")

        self.conn.executescript(script)

    # -------------------------
    # Lectura
    # -------------------------

    def fetchone(
        self,
        query: str,
        params: Iterable[Any] = ()
    ) -> Optional[sqlite3.Row]:
        """
        Ejecuta una consulta SELECT y devuelve una fila.
        """
        cursor = self.execute(query, params)
        return cursor.fetchone()

    def fetchall(
        self,
        query: str,
        params: Iterable[Any] = ()
    ) -> list[sqlite3.Row]:
        """
        Ejecuta una consulta SELECT y devuelve todas las filas.
        """
        cursor = self.execute(query, params)
        return cursor.fetchall()
