from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.crud import crud_user
from app.db.base import get_db
from app.schemas import user as user_schema
from app.db.models import user as user_model
from app.core.security import get_current_user
router = APIRouter()

@router.get("/me", response_model=user_schema.User)
def read_users_me(
    current_user: user_model.User = Depends(get_current_user)
):
    return current_user

@router.get("/leaderboard", response_model=List[user_schema.User])
def read_leaderboard(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    leaderboard_users = crud_user.get_users_sorted_by_score(db, skip=skip, limit=limit)
    return leaderboard_users