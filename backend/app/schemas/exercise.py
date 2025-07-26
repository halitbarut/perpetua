from pydantic import BaseModel, Field
from typing import List, Literal

class GrammarQuestion(BaseModel):
    sentence_template: str
    word_bank: List[str]
    correct_word: str

class ExerciseSession(BaseModel):
    exercise_type: Literal["grammar", "dialogue", "word_matching"]
    questions: List[GrammarQuestion]

class WrongAnswerPayload(BaseModel):
    question: str
    user_answer: str
    correct_answer: str

class ExerciseResultPayload(BaseModel):
    total_questions: int
    correct_answers: int
    wrong_answers: List[WrongAnswerPayload]

class EvaluationResult(BaseModel):
    score: int = Field(..., ge=0, le=100)
    feedback: str