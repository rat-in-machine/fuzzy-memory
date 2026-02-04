from sql.sqlite import SQLiteDB
from typing import List, Optional
import sqlite3

class WishlistDAO:
    
    def __init__(self, db: SQLiteDB):
        self.db = db

    def add(self, user_id: int, appid: int) -> None:
        self.db.execute(
            "INSERT INTO Wishlist (user_id, appid) VALUES (?, ?)",
            (user_id, appid)
        )

    def remove(self, user_id: int, appid: int) -> None:
        self.db.execute(
            "DELETE FROM Wishlist WHERE user_id = ? AND appid = ?",
            (user_id, appid)
        )

    def list_by_user(self, user_id: int) -> List[sqlite3.Row]:
        return self.db.fetchall(
            """
            SELECT w.*, g.name as game_name
            FROM Wishlist w
            JOIN Game g ON w.appid = g.appid
            WHERE w.user_id = ?
            """,
            (user_id,)
        )
