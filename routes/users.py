# routes/user_routes.py
from fastapi import APIRouter, HTTPException
from typing import List
from sql.sqlite import SQLiteDB
from structures.dao.user_dao import UserDAO

router = APIRouter(prefix="/users", tags=["users"])

db = SQLiteDB("app.db")
user_dao = UserDAO(db)

@router.post("/", response_model=int)
def create_user(name: str, password: str, email: str, role_id: int):
    user_id = user_dao.create(name, password, email, role_id)
    if user_id == -1:
        raise HTTPException(status_code=400, detail="No se pudo crear el usuario")
    return user_id

@router.get("/{user_id}", response_model=dict)
def get_user(user_id: int):
    row = user_dao.get(user_id)
    if not row:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return dict(row)

@router.get("/", response_model=List[dict])
def list_users():
    return [dict(u) for u in user_dao.list_all()]

@router.get("/{user_id}/with_role", response_model=dict)
def get_user_with_role(user_id: int):
    row = user_dao.get_with_role(user_id)
    if not row:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    user = {k: row[k] for k in ["id", "name", "password", "email", "role_id"]}
    role = {k: row[k] for k in ["role_name", "can_query", "can_insert", "can_update", "can_delete"]}
    return {"user": user, "role": role}
