from sqlalchemy import desc
from sqlalchemy.orm import Session
from app.db.models import user as model
from app.schemas import user as schema
from app.core.security import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(model.User).filter(model.User.email == email).first()

def create_user(db: Session, user: schema.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = model.User(
        email=user.email,
        username=user.username,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(model.User).filter(model.User.username == username).first()

def get_users_sorted_by_score(db: Session, skip: int = 0, limit: int = 100):
    return db.query(model.User).order_by(desc(model.User.weekly_score)).offset(skip).limit(limit).all()