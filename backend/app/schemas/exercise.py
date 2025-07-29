from pydantic import BaseModel, Field
from typing import List, Literal, Dict, Union, Annotated

class GrammarQuestion(BaseModel):
    type: Literal["grammar"] = "grammar"
    sentence_template: str
    word_bank: List[str]
    correct_word: str

class DialogueQuestion(BaseModel):
    type: Literal["dialogue"] = "dialogue"
    dialogue: List[Dict[str, str]]
    question: str
    options: List[str]
    correct_answer: str

class WordMatchingSet(BaseModel):
    type: Literal["word_matching"] = "word_matching"
    topic: str
    words: List[str]
    meanings: List[str]

AnyQuestion = Annotated[
    Union[GrammarQuestion, DialogueQuestion, WordMatchingSet],
    Field(discriminator="type"),
]

class ExerciseSession(BaseModel):
    exercise_type: Literal["grammar", "dialogue", "word_matching"]
    questions: List[AnyQuestion]

class ExerciseSession(BaseModel):
    exercise_type: Literal["grammar", "dialogue", "word_matching"]
    questions: List[AnyQuestion]

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

from typing import Union, Annotated

AnyQuestion = Annotated[
    Union[GrammarQuestion, DialogueQuestion, WordMatchingSet],
    Field(discriminator="type"),
]