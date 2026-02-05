import os
from dotenv import load_dotenv

import fastapi

from sql.azure_sqldb import AzureSQLDB  # clase de conexión a Azure SQL

from structures.dao.game_dao import GameDAO
from structures.dao.wish_dao import WishlistDAO
from structures.dao.roles_dao import RoleDAO
from structures.dao.user_dao import UserDAO

from routes import games, wishlist, role, users

load_dotenv()

# =====================================================
# CONFIGURACIÓN DE AZURE SQL
# =====================================================
AZURE_SQL_SERVER = os.getenv("AZURE_SQL_SERVER") or ""
AZURE_SQL_SERVER_DATABASE = os.getenv("AZURE_SQL_SERVER_DATABASE") or ""
AZURE_SQL_SERVER_USERNAME = os.getenv("AZURE_SQL_SERVER_USERNAME") or ""
AZURE_SQL_SERVER_PASSWORD = os.getenv("AZURE_SQL_SERVER_PASSWORD") or ""

# =====================================================
# INICIALIZAR LA APLICACIÓN FASTAPI
# =====================================================
app = fastapi.FastAPI(title="Steam API")

# =====================================================
# CONEXIÓN A AZURE SQL
# =====================================================
db = AzureSQLDB(AZURE_SQL_SERVER, AZURE_SQL_SERVER_DATABASE, AZURE_SQL_SERVER_USERNAME, AZURE_SQL_SERVER_PASSWORD)
db.connect()  # conexión abierta durante el ciclo de vida de la app

# =====================================================
# INICIALIZAR DAOS
# =====================================================
game_dao = GameDAO(db)
wishlist_dao = WishlistDAO(db)
role_dao = RoleDAO(db)
user_dao = UserDAO(db)

# =====================================================
# INYECTAR DAOS EN ROUTERS
# =====================================================
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

# from sql.azure_sqldb import AzureSQLDB
# from structures.dao.game_dao import GameDAO
# from structures.dao.roles_dao import RoleDAO
# from structures.dao.user_dao import UserDAO
# from structures.dao.wish_dao import WishlistDAO

# import os

# # =====================================================
# # CONFIGURACIÓN AZURE SQL
# # =====================================================
# SERVER = "db-zelmar.database.windows.net"
# DATABASE = "covid"
# USERNAME = "user"
# PASSWORD = "Kebab123!"

# # =====================================================
# # CONEXIÓN
# # =====================================================
# db = AzureSQLDB(SERVER, DATABASE, USERNAME, PASSWORD)
# db.connect()

# # =====================================================
# # INICIALIZAR DAOs
# # =====================================================
# game_dao = GameDAO(db)
# role_dao = RoleDAO(db)
# user_dao = UserDAO(db)
# wishlist_dao = WishlistDAO(db)

# # =====================================================
# # PRUEBAS: list_all()
# # =====================================================
# print("=== GAMES ===")
# games = game_dao.list_all()
# for g in games:
#     print(f"{g.appid}: {g.name} - {g.final_price} {g.currency}")

# print("\n=== ROLES ===")
# roles = role_dao.list_all()
# for r in roles:
#     print(f"{r.id}: {r.name} - SELECT:{r.can_query} INSERT:{r.can_insert} UPDATE:{r.can_update} DELETE:{r.can_delete}")

# print("\n=== USERS ===")
# users = user_dao.list_all()
# for u in users:
#     print(f"{u.id}: {u.name} ({u.email}) - role_id: {u.role_id}")

# print("\n=== WISHLIST ===")
# # Para wishlist mostramos user_id + appid + nombre del juego
# for u in users:
#     items = wishlist_dao.list_by_user(u.id)
#     print(f"Wishlist for user {u.name}:")
#     if items:
#         for w in items:
#             print(f"  - {w.appid}: {w.game_name}")
#     else:
#         print("  (empty)")

# # =====================================================
# # Cerrar conexión
# # =====================================================
# db.close()

