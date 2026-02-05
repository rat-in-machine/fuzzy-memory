from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, cast
from structures.dao.wish_dao import WishlistDAO
from structures.dao.game_dao import GameDAO

router = APIRouter()
wishlist_dao: WishlistDAO = cast(WishlistDAO, None) 
game_dao: GameDAO = cast(GameDAO, None)             

class WishlistItem(BaseModel):
    user_id: int
    appid: int

@router.post("/", tags=["wishlist"])
def add_wishlist(item: WishlistItem):
    """
    Agrega un juego a la lista de deseados de un usuario.
    
    :param item: Objeto a agregar a la base de datos.
    :type item: WishlistItem
    """
    game = game_dao.get(item.appid)
    if not game:
        raise HTTPException(status_code=404, detail="Game not found")
    wishlist_dao.add(item.user_id, item.appid)
    return {"message": "Added to wishlist"}

@router.get("/{user_id}", response_model=List[dict], tags=["wishlist"])
def get_wishlist(user_id: int):
    """
    Consulta la lista de deseados de un usuario.
    
    :param user_id: Description
    :type user_id: int
    """
    rows = wishlist_dao.list_by_user(user_id)
    return [
        {"appid": row["appid"], "name": row["game_name"]}
        for row in rows
    ]
