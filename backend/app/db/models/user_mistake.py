from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class UserMistake(Base):
    __tablename__ = "user_mistakes"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(String, index=True)
    user_answer = Column(String)
    correct_answer = Column(String)

    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="mistakes")