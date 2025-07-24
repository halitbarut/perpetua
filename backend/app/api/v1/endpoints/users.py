from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas import user as user_schema
from app.db.models import user as user_model
from app.core.security import get_current_user

router = APIRouter()

@router.get("/me", response_model=user_schema.User)
def read_users_me(
    current_user: user_model.User = Depends(get_current_user)
):
    return current_user