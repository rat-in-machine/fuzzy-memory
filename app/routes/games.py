from fastapi import APIRouter, Depends, HTTPException
import json

from app.auth.dependencies import get_current_user, require_role

router = APIRouter(
    prefix="/games",
    tags=["Games"]
)

DATA_FILE = "app/data/games.json"


def load_games():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="Games file not found")


# 🔒 PROTEGIDO CON JWT
@router.get("", dependencies=[Depends(get_current_user)])
def get_games():
    """
    Devuelve todos los juegos.
    Requiere usuario autenticado.
    """
    return load_games()


# 🔒 PROTEGIDO CON JWT
@router.get("/{game_id}", dependencies=[Depends(get_current_user)])
def get_game_by_id(game_id: int):
    """
    Devuelve un juego por ID.
    Requiere usuario autenticado.
    """
    games = load_games()

    for game in games:
        if game["id"] == game_id:
            return game

    raise HTTPException(status_code=404, detail="Game not found")


# 🔐 SOLO ADMIN
@router.post("", dependencies=[Depends(require_role("admin"))])
def create_game(game: dict):
    """
    Crear juego (solo admin)
    """
    games = load_games()
    new_id = max(g["id"] for g in games) + 1 if games else 1
    game["id"] = new_id

    games.append(game)

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(games, f, indent=2, ensure_ascii=False)

    return {"message": "Game created", "game": game}


# 🔐 SOLO ADMIN
@router.delete("/{game_id}", dependencies=[Depends(require_role("admin"))])
def delete_game(game_id: int):
    """
    Eliminar juego (solo admin)
    """
    games = load_games()
    new_games = [g for g in games if g["id"] != game_id]

    if len(new_games) == len(games):
        raise HTTPException(status_code=404, detail="Game not found")

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(new_games, f, indent=2, ensure_ascii=False)

    return {"message": "Game deleted"}
