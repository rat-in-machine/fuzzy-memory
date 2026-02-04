from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Wishlist
from app.auth.dependencies import get_current_user
from app.db.models import User

router = APIRouter(
    prefix="/wishlist",
    tags=["Wishlist"]
)

@router.get("/")
def get_my_wishlist(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    print("🟢 ENTRA EN WISHLIST")
    print("🟢 USER:", current_user)

    return {
        "user_id": current_user.id,
        "message": "Wishlist endpoint works"
    }

