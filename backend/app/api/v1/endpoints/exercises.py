from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Literal

from app import schemas, services
from app.db import models
from app.db.base import get_db
from app.core.security import get_current_user

router = APIRouter()

ExerciseType = Literal["grammar", "dialogue", "word_matching"]

@router.get("/", response_model=schemas.exercise.Exercise)
def get_new_exercise(
    exercise_type: ExerciseType = Query(..., description="Oluşturulacak alıştırma tipi"),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    exercise = services.gemini_service.create_exercise_from_ai(exercise_type)

    if not exercise or "error" in exercise:
        raise HTTPException(
            status_code=500,
            detail=f"AI'dan '{exercise_type}' alıştırması oluşturulamadı."
        )
    return exercise