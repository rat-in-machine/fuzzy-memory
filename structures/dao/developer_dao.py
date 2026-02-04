from sql.sqlite import SQLiteDB
from typing import List, Optional
import sqlite3

class DeveloperDAO:
    def __init__(self, db: SQLiteDB):
        self.db = db

    def create(self, name: str) -> int:
        cursor = self.db.execute(
            "INSERT INTO Developer (name) VALUES (?)",
            (name,)
        )
        
        lastId = cursor.lastrowid
        result = -1 if not lastId else lastId
        
        return result
    
    def get(self, dev_id: int) -> Optional[sqlite3.Row]:
        return self.db.fetchone("SELECT * FROM Developer WHERE id = ?", (dev_id,))

    def list_all(self) -> List[sqlite3.Row]:
        return self.db.fetchall("SELECT * FROM Developer")
