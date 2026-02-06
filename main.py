import os
from dotenv import load_dotenv

import fastapi

from sql.azure_sqldb import AzureSQLDB  # clase de conexión a Azure SQL

from structures.dao.game_dao import GameDAO
from structures.dao.wish_dao import WishlistDAO
from structures.dao.roles_dao import RoleDAO
from structures.dao.user_dao import UserDAO

from routes.chat import router as chat_router

from routes import games, wishlist, role, users
# from utils.config import (
#     AZURE_SQL_SERVER, AZURE_SQL_SERVER_DATABASE,
#     AZURE_SQL_SERVER_USERNAME, AZURE_SQL_SERVER_PASSWORD
# )
from utils.config import AZURE_SQL_SERVER
from utils.config import AZURE_SQL_SERVER_DATABASE
from utils.config import AZURE_SQL_SERVER_USERNAME
from utils.config import AZURE_SQL_SERVER_PASSWORD

load_dotenv()

# # =====================================================
# # CONFIGURACIÓN DE AZURE SQL
# # =====================================================


# # =====================================================
# # INICIALIZAR LA APLICACIÓN FASTAPI
# # =====================================================
app = fastapi.FastAPI(title="Steam API")

# # =====================================================
# # CONEXIÓN A AZURE SQL
# # =====================================================
db = AzureSQLDB(AZURE_SQL_SERVER, AZURE_SQL_SERVER_DATABASE, AZURE_SQL_SERVER_USERNAME, AZURE_SQL_SERVER_PASSWORD)
db.connect()  # conexión abierta durante el ciclo de vida de la app

# # =====================================================
# # INICIALIZAR DAOS
# # =====================================================
game_dao = GameDAO(db)
wishlist_dao = WishlistDAO(db)
role_dao = RoleDAO(db)
user_dao = UserDAO(db)

# # =====================================================
# # INYECTAR DAOS EN ROUTERS
# # =====================================================
if hasattr(games, "game_dao"):
    games.game_dao = game_dao
else:
    raise RuntimeError("games router no tiene atributo game_dao")

if hasattr(wishlist, "wishlist_dao"):
    wishlist.wishlist_dao = wishlist_dao
else:
    raise RuntimeError("wishlist router no tiene atributo wishlist_dao")

if hasattr(wishlist, "game_dao"):
    wishlist.game_dao = game_dao
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

# =====================================================
# INCLUIR ROUTERS
# =====================================================
app.include_router(games.router, prefix="/games", tags=["games"])
app.include_router(wishlist.router, prefix="/wishlist", tags=["wishlist"])
app.include_router(role.router, prefix="/roles", tags=["roles"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(chat_router)


