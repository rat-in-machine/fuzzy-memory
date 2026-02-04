from pydantic import BaseModel
from typing import List

class Game(BaseModel):
    id: int
    name: str
    genres: List[str]
    developer: str
