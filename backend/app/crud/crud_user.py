from sqlalchemy.orm import Session
from sqlalchemy import desc

from app.db.models import user as model_user, user_mistake as model_mistake
from app.schemas import user as schema_user
from app.schemas import exercise as schema_exercise
from app.core.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(model_user.User).filter(model_user.User.email == email).first()

def get_user_by_username(db: Session, username: str):
    return db.query(model_user.User).filter(model_user.User.username == username).first()

def create_user(db: Session, user: schema_user.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = model_user.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_users_sorted_by_score(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model_user.User).order_by(desc(model_user.User.weekly_score)).offset(skip).limit(limit).all()

def create_user_mistake(db: Session, user_id: int, mistake_in: schema_exercise.WrongAnswerPayload):
    """Kullanıcının yaptığı bir hatayı veritabanına kaydeder."""
    db_mistake = model_mistake.UserMistake(
        question_text=mistake_in.question,
        user_answer=mistake_in.user_answer,
        correct_answer=mistake_in.correct_answer,
        owner_id=user_id
    )
    db.add(db_mistake)
    db.commit()
    return db_mistake