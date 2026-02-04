from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from typing import List, Optional, cast
from structures.dao.game_dao import GameDAO  # Tu DAO ya hecho

router = APIRouter()
game_dao: GameDAO = cast(GameDAO, None)

class GameCreate(BaseModel):
    appid: int
    name: str
    short_description: Optional[str] = None
    currency: Optional[str] = None
    initial_price: Optional[float] = None
    final_price: Optional[float] = None
    discount_percent: Optional[int] = None
    is_free: bool = False
    windows: bool = True
    mac: bool = False
    linux: bool = False

class GameResponse(BaseModel):
    appid: int
    name: str
    short_description: Optional[str]
    is_free: bool

@router.post("/", response_model=GameResponse)
def create_game(game: GameCreate):
    existing = game_dao.get(game.appid)
    if existing:
        raise HTTPException(status_code=400, detail="Game already exists")
    game_dao.create(
        appid=game.appid,
        name=game.name,
        short_description=game.short_description or "",
        currency=game.currency,
        initial_price=game.initial_price,
        final_price=game.final_price,
        discount_percent=game.discount_percent,
        is_free=game.is_free,
        windows=game.windows,
        mac=game.mac,
        linux=game.linux
    )
    return GameResponse(
        appid=game.appid,
        name=game.name,
        short_description=game.short_description,
        is_free=game.is_free
    )

@router.get("/", response_model=List[GameResponse])
def list_games():
    rows = game_dao.list_all()
    return [
        GameResponse(
            appid=row["appid"],
            name=row["name"],
            short_description=row["short_description"],
            is_free=bool(row["is_free"])
        ) for row in rows
    ]
