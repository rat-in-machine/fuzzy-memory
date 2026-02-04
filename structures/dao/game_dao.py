from sql.sqlite import SQLiteDB
from typing import List, Optional
import sqlite3

class GameDAO:
    def __init__(self, db: SQLiteDB):
        self.db = db

    def create(self, appid: int, name: str, short_description: str,
               currency: Optional[str], initial_price: Optional[float],
               final_price: Optional[float], discount_percent: Optional[int],
               is_free: bool,
               windows: bool, mac: bool, linux: bool) -> None:
        self.db.execute(
            """
            INSERT INTO Games
            (appid, name, short_description, currency, initial_price,
             final_price, discount_percent, is_free, windows, mac, linux)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (appid, name, short_description, currency, initial_price,
             final_price, discount_percent, int(is_free),
             int(windows), int(mac), int(linux))
        )

    def get(self, appid: int) -> Optional[sqlite3.Row]:
        return self.db.fetchone("SELECT * FROM Games WHERE appid = ?", (appid,))

    def list_all(self) -> List[sqlite3.Row]:
        return self.db.fetchall("SELECT * FROM Games")

    def delete(self, appid: int) -> None:
        self.db.execute("DELETE FROM Games WHERE appid = ?", (appid,))
