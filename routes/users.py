from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, cast

from structures.dao.user_dao import UserDAO

router = APIRouter(prefix="/users", tags=["users"])

user_dao: UserDAO = cast(UserDAO, None)

class UserCreate(BaseModel):
    name: str
    password: str
    email: str
    role_id: int

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role_id: int

class UserWithRoleResponse(BaseModel):
    user: dict
    role: dict
    
class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/create", response_model=int)
def create_user(user: UserCreate):
    user_id = user_dao.create(
        name=user.name,
        password=user.password,
        email=user.email,
        role_id=user.role_id
    )

    if user_id == -1:
        raise HTTPException(status_code=400, detail="No se pudo crear el usuario")

    return user_id

@router.get("/get/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    row = user_dao.get(user_id)
    if not row:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    return UserResponse(
        id=row[0],
        name=row[1],
        email=row[3],
        role_id=row[4]
    )

@router.delete("/delete/{user_id}", response_model=dict)
def delete_user(user_id: int):
    """
    Elimina un usuario por su ID.
    """
    success = user_dao.delete(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return {"detail": f"Usuario con ID {user_id} eliminado correctamente"}

@router.get("/list", response_model=List[UserResponse])
def list_users():
    rows = user_dao.list_all()

    return [
        UserResponse(
            id=int(row[0]),
            name=row[1],
            email=row[3],
            role_id=int(row[4])
        )
        for row in rows
    ]

@router.get("/get_with_role/{user_id}", response_model=UserWithRoleResponse)
def get_user_with_role(user_id: int):
    row = user_dao.get_with_role(user_id)
    if not row:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user = {
        "id": row[0],
        "name": row[1],
        "email": row[3],
        "role_id": row[5]   # aquí es el id del rol
    }

    role = {
        "name": row[4],
        "can_query": row[6],
        "can_insert": row[7],
        "can_update": row[8],
        "can_delete": row[9]
    }

    return {"user": user, "role": role}

@router.post("/login")
def login_user(data: LoginRequest):
    """
    Verifica las credenciales del usuario.
    
    :param data: Información del usuario.
    :type data: LoginRequest
    """
    
    user = user_dao.get_by_email(data.email)

    if not user:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    if user[2] != data.password:
        raise HTTPException(status_code=401, detail="Credenciales inválidas")

    return {
        "id": user[0],
        "name": user[1],
        "email": user[3],
        "role_id": user[4]
    }
