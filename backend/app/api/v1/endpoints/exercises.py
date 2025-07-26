from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Literal

from app.services import gemini_service
from app.schemas.exercise import ExerciseSession, EvaluationResult, ExerciseResultPayload
from app.db.models import user as user_model, user_mistake as user_mistake_model
from app.db.base import get_db
from app.core.security import get_current_user

router = APIRouter()

ExerciseType = Literal["grammar", "dialogue", "word_matching"]

@router.get("/", response_model=ExerciseSession)
def get_new_exercise(
    exercise_type: ExerciseType = Query(..., description="Oluşturulacak alıştırma tipi"),
    db: Session = Depends(get_db),
    current_user: user_model.User = Depends(get_current_user)
):
    ai_response = gemini_service.create_exercise_from_ai(exercise_type)

    if not ai_response or "questions" not in ai_response:
        raise HTTPException(
            status_code=500,
            detail=f"AI'dan '{exercise_type}' alıştırması oluşturulamadı."
        )

    return ExerciseSession(
        exercise_type=exercise_type,
        questions=ai_response["questions"]
    )


@router.post("/evaluate", response_model=EvaluationResult)
def evaluate_exercise(
        payload: ExerciseResultPayload,
        db: Session = Depends(get_db),
        current_user: user_model.User = Depends(get_current_user)
):
    evaluation = gemini_service.evaluate_exercise_from_ai(
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
        db_mistake = user_mistake_model.UserMistake(
            question_text=mistake.question,
            user_answer=mistake.user_answer,
            correct_answer=mistake.correct_answer,
            owner_id=current_user.id
        )
        db.add(db_mistake)

    db.commit()
    db.refresh(current_user)

    return evaluation