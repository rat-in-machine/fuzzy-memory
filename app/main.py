from fastapi import FastAPI
from app.auth.router import router as auth_router
from app.routes import games, wishlist
from app.db.database import Base, engine
from app.db import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fuzzy Memori API", version="1.0.0")

@app.get("/")
def root():
    return {"message": "Fuzzy Memori API is running 🚀"}

app.include_router(auth_router)
app.include_router(games.router)
app.include_router(wishlist.router)
