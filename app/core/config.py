# app/core/config.py

from datetime import timedelta

# ⚠️ NO usamos .env porque vuestro .env no tiene JWT
# Esto es SOLO para autenticación local del backend

SECRET_KEY = "fuzzy-memori-super-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60
