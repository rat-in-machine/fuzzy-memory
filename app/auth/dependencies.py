from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session

from app.core.config import SECRET_KEY, ALGORITHM
from app.db.database import get_db
from app.db.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str | None = payload.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401)

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication token"
        )

    user = db.query(User).filter(User.id == int(user_id)).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user


# ✅ ESTA ES LA FUNCIÓN QUE FALTABA
def require_role(required_role: str):
    def role_checker(user: User = Depends(get_current_user)):
        # Si tu User NO tiene roles, dejamos pasar (modo simple)
        # Puedes ampliar esto luego
        if hasattr(user, "role"):
            if user.role != required_role:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions"
                )
        return user

    return role_checker
