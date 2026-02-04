from sql.sqlite import SQLiteDB
from typing import List, Optional
import sqlite3

class GenreDAO:
    def __init__(self, db: SQLiteDB):
        self.db = db

    def create(self, genre_id: str, description: str) -> None:
        self.db.execute(
            "INSERT INTO Genre (id, description) VALUES (?, ?)",
            (genre_id, description)
        )

    def get(self, genre_id: str) -> Optional[sqlite3.Row]:
        return self.db.fetchone("SELECT * FROM Genre WHERE id = ?", (genre_id,))

    def list_all(self) -> List[sqlite3.Row]:
        return self.db.fetchall("SELECT * FROM Genre")
