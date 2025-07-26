from pydantic import BaseModel
from typing import Dict

class Exercise(BaseModel):
    question: str
    options: Dict[str, str]
    correct_answer: str