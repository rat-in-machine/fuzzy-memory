from fastapi import APIRouter
from src.services.game_search import get_game_search

router = APIRouter()

game_search = get_game_search()

@router.get("/search-game", tags=["Search"])
async def search_game(name: str, limit: int = 5):
    games = game_search.search_by_name(name, limit)
    return {"query": name, "found": len(games), "results": games}

@router.get("/search-by-genre", tags=["Search"])
async def search_by_genre(genre: str, limit: int = 5):
    games = game_search.search_by_genre(genre, limit)
    return {"genre": genre, "found": len(games), "results": games}
