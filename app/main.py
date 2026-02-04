from fastapi import FastAPI
from app.routes import games
from app.auth import router as auth_router
from app.db.database import engine
from app.db import models

# Crear tablas SQLite
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Fuzzy Memori API",
    version="1.0.0"
)

@app.get("/")
async def root():
    return {"message": "Fuzzy Memori API is running 🚀"}

# Rutas
app.include_router(games.router)
app.include_router(auth_router.router)
