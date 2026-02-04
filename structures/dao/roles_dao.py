from sql.sqlite import SQLiteDB
from typing import List, Optional
import sqlite3

class RoleDAO:

    def __init__(self, db: SQLiteDB):
        self.db = db

    def create(self, name: str, can_select: int = 0, can_insert: int = 0, can_update: int = 0, can_delete: int = 0) -> int:
        cursor = self.db.execute(
            "INSERT INTO Role (name, can_query, can_insert, can_update, can_delete) VALUES (?, ?, ?, ?, ?)",
            (name, can_select, can_insert, can_update, can_delete)
        )
        lastId = cursor.lastrowid
        return -1 if not lastId else lastId

    def get(self, role_id: int) -> Optional[sqlite3.Row]:
        return self.db.fetchone("SELECT * FROM Role WHERE id = ?", (role_id,))

    def list_all(self) -> List[sqlite3.Row]:
        return self.db.fetchall("SELECT * FROM Role")
