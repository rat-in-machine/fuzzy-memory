from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, cast

from structures.dao.roles_dao import RoleDAO

router = APIRouter()

# Será asignado desde main.py
role_dao: RoleDAO = cast(RoleDAO, None)


class RoleCreate(BaseModel):
    name: str
    can_select: int = 0
    can_insert: int = 0
    can_update: int = 0
    can_delete: int = 0


class RoleResponse(BaseModel):
    id: int
    name: str
    can_query: int
    can_insert: int
    can_update: int
    can_delete: int


@router.post("/", response_model=int)
def create_role(role: RoleCreate):
    role_id = role_dao.create(
        name=role.name,
        can_select=role.can_select,
        can_insert=role.can_insert,
        can_update=role.can_update,
        can_delete=role.can_delete,
    )

    if role_id == -1:
        raise HTTPException(status_code=400, detail="No se pudo crear el rol")

    return role_id


@router.get("/{role_id}", response_model=RoleResponse)
def get_role(role_id: int):
    row = role_dao.get(role_id)
    if not row:
        raise HTTPException(status_code=404, detail="Rol no encontrado")

    return RoleResponse(
        id=row[0],
        name=row[1],
        can_query=row[2],
        can_insert=row[3],
        can_update=row[4],
        can_delete=row[5],
    )


@router.get("/", response_model=List[RoleResponse])
def list_roles():
    rows = role_dao.list_all()

    return [
        RoleResponse(
            id=row[0],
            name=row[1],
            can_query=row[2],
            can_insert=row[3],
            can_update=row[4],
            can_delete=row[5],
        )
        for row in rows
    ]
