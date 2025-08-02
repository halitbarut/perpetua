from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Literal

from app import services
from app.db.models import user
from app.schemas import exercise as exercise_schema
from app.db import models as user_model
from app.crud import crud_user
from app.db.base import get_db
from app.core.security import get_current_user
from app.services import gemini_service

router = APIRouter()

ExerciseType = Literal["grammar", "dialogue", "word_matching"]

@router.get("/", response_model=exercise_schema.ExerciseSession)
def get_new_exercise(
    exercise_type: ExerciseType = Query(..., description="Oluşturulacak alıştırma tipi"),
    db: Session = Depends(get_db),
    current_user: user_model.user.User = Depends(get_current_user)
):
    ai_response = gemini_service.create_exercise_from_ai(
        exercise_type=exercise_type
    )
    if not ai_response or "questions" not in ai_response:
        raise HTTPException(
            status_code=500,
            detail=f"AI'dan '{exercise_type}' alıştırması oluşturulamadı."
        )
    return exercise_schema.ExerciseSession(
        exercise_type=exercise_type,
        questions=ai_response["questions"]
    )

@router.post("/evaluate", response_model=exercise_schema.EvaluationResult)
def evaluate_exercise(
    payload: exercise_schema.EvaluationPayload,
    db: Session = Depends(get_db),
    current_user: user.User = Depends(get_current_user)
):
    evaluation = services.gemini_service.evaluate_exercise_from_ai(
        results=payload.dict(),
        username=current_user.username
    )
    if not evaluation:
        raise HTTPException(
            status_code=500,
            detail="AI'dan değerlendirme sonucu alınamadı."
        )
    current_user.weekly_score += evaluation["score"]
    for mistake in payload.wrong_answers:
        crud_user.create_user_mistake(db=db, user_id=current_user.id, mistake_in=mistake)
    crud_user.delete_oldest_mistakes(db=db, user_id=current_user.id, keep_limit=50)
    db.commit()
    db.refresh(current_user)
    return evaluation