# routes/role_routes.py
from fastapi import APIRouter, HTTPException
from typing import List
from sql.sqlite import SQLiteDB
from structures.dao.roles_dao import RoleDAO

router = APIRouter(prefix="/roles", tags=["roles"])

db = SQLiteDB("app.db")
role_dao = RoleDAO(db)

@router.post("/", response_model=int)
def create_role(name: str, can_select: int = 0, can_insert: int = 0, can_update: int = 0, can_delete: int = 0):
    role_id = role_dao.create(name, can_select, can_insert, can_update, can_delete)
    if role_id == -1:
        raise HTTPException(status_code=400, detail="No se pudo crear el rol")
    return role_id

@router.get("/{role_id}", response_model=dict)
def get_role(role_id: int):
    row = role_dao.get(role_id)
    if not row:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return dict(row)

@router.get("/", response_model=List[dict])
def list_roles():
    return [dict(r) for r in role_dao.list_all()]
