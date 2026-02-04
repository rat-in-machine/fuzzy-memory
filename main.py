import os
import fastapi

from sql.sqlite import SQLiteDB

from structures.dao.game_dao import GameDAO
from structures.dao.wish_dao import WishlistDAO
from structures.dao.roles_dao import RoleDAO
from structures.dao.user_dao import UserDAO

from routes import games, wishlist, role, users

DB_FILE = "data.sql"
SQL_CREATE_FILE = "sql/create_tables.sql"

app = fastapi.FastAPI(title="Steam API")

if not os.path.exists(DB_FILE):
    db = SQLiteDB(DB_FILE)
    db.connect()
    with open(SQL_CREATE_FILE, "r", encoding="utf-8") as f:
        db.executescript(f.read())  # crear tablas si no existe el archivo
    db.close()

db = SQLiteDB(DB_FILE)
db.connect()  # conexión abierta durante todo el ciclo de vida de la app

game_dao = GameDAO(db)  # inicializar DAO de juegos
wishlist_dao = WishlistDAO(db)  # inicializar DAO de wishlist
role_dao = RoleDAO(db)      # DAO de roles
user_dao = UserDAO(db)      # DAO de usuarios

if hasattr(games, "game_dao"):
    games.game_dao = game_dao  # inyectar DAO en router games
else:
    raise RuntimeError("games router no tiene atributo game_dao")

if hasattr(wishlist, "wishlist_dao"):
    wishlist.wishlist_dao = wishlist_dao  # inyectar DAO en router wishlist
else:
    raise RuntimeError("wishlist router no tiene atributo wishlist_dao")

if hasattr(wishlist, "game_dao"):
    wishlist.game_dao = game_dao  # inyectar DAO de juegos en wishlist para validaciones
else:
    raise RuntimeError("wishlist router no tiene atributo game_dao")

if hasattr(role, "role_dao"):
    role.role_dao = role_dao
else:
    raise RuntimeError("role router no tiene atributo role_dao")

if hasattr(users, "user_dao"):
    users.user_dao = user_dao
else:
    raise RuntimeError("user router no tiene atributo user_dao")


app.include_router(games.router, prefix="/games", tags=["games"])
app.include_router(wishlist.router, prefix="/wishlist", tags=["wishlist"])
app.include_router(role.router, prefix="/roles", tags=["roles"])
app.include_router(users.router, prefix="/users", tags=["users"])
