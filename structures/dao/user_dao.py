from sql.sqlite import SQLiteDB
from typing import List, Optional
import sqlite3

class UserDAO:

    def __init__(self, db: SQLiteDB):
        self.db = db

    def create(self, name: str, password: str, email: str, role_id: int) -> int:
        cursor = self.db.execute(
            "INSERT INTO User (name, password, email, role_id) VALUES (?, ?, ?, ?)",
            (name, password, email, role_id)
        )
        lastId = cursor.lastrowid
        return -1 if not lastId else lastId

    def get(self, user_id: int) -> Optional[sqlite3.Row]:
        return self.db.fetchone("SELECT * FROM User WHERE id = ?", (user_id,))

    def list_all(self) -> List[sqlite3.Row]:
        return self.db.fetchall("SELECT * FROM User")

    def get_with_role(self, user_id: int) -> Optional[sqlite3.Row]:
        return self.db.fetchone("""
            SELECT u.*, r.name AS role_name, r.can_query, r.can_insert, r.can_update, r.can_delete
            FROM User u
            JOIN Role r ON u.role_id = r.id
            WHERE u.id = ?
        """, (user_id,))
