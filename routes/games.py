from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from dataclasses import asdict

from structures.gg_deal_game import GGDealGame
from utils.gg_deals_requests import GGDealsPricesAPI
from fastapi import Path


from typing import List, Dict, Optional, cast
from structures.dao.game_dao import GameDAO 

router = APIRouter()
game_dao: GameDAO = cast(GameDAO, None)

gg_api = GGDealsPricesAPI(api_key="10u0ii_6ldE5msBBWXNdy6iuLPfAQTEi")

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
    currency: Optional[str]
    initial_price: Optional[float]
    final_price: Optional[float]
    discount_percent: Optional[int]
    is_free: bool
    windows: bool
    mac: bool
    linux: bool

@router.get("/{appid}", response_model=GameResponse)
def get_game(appid: int = Path(..., description="AppID del juego a consultar")):
    row = game_dao.get(appid)
    if not row:
        raise HTTPException(status_code=404, detail="Game not found")

    return GameResponse(
        appid=int(row[0]),
        name=row[1],
        short_description=row[2],
        currency=row[3],
        initial_price=row[4],
        final_price=row[5],
        discount_percent=row[6],
        is_free=bool(row[7]),
        windows=bool(row[8]),
        mac=bool(row[9]),
        linux=bool(row[10])
    )

@router.delete("/{appid}", response_model=dict)
def delete_game(appid: int = Path(..., description="AppID del juego a eliminar")):
    """
    Elimina un juego por su AppID.
    """
    row = game_dao.get(appid)
    if not row:
        raise HTTPException(status_code=404, detail="Game not found")
    
    game_dao.delete(appid)
    return {"detail": f"Game with appid {appid} deleted successfully"}




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

@router.get("/", response_model=List[GameResponse])
def list_games():
    rows = game_dao.list_all()

    return [
        GameResponse(
            appid=int(row[0]),
            name=row[1],
            short_description=row[2],
            currency=row[3],
            initial_price=row[4],
            final_price=row[5],
            discount_percent=row[6],
            is_free=bool(row[7]),
            windows=bool(row[8]),
            mac=bool(row[9]),
            linux=bool(row[10])
        ) for row in rows
    ]

@router.get("/historical-lows")
def get_historical_lows(
    appids: List[int] = Query(..., description="Lista de Steam AppIDs (máx 100)")
) -> Dict[int, GGDealGame]:
    """
    Obtiene el mínimo historico de 1 o más juegos. 
    
    :param appids: appID del videojuego a consultar.
    :type appids: List[int]
    :return: Lista de videojuegos y precio mínimo histórico.
    :rtype: Dict[int, GGDealGame]
    """
    
    if not appids:
        raise HTTPException(status_code=400, detail="AppIDs list cannot be empty")

    try:
        data = gg_api.get_prices_by_appids(appids)
    except Exception as e:
        raise HTTPException(status_code=502, detail=str(e))

    result: Dict[int, GGDealGame] = {}

    for appid, game in data.items():
        if game is None:
            continue

        result[appid] = game

    return result
