from typing import List, Optional
from pydantic import BaseModel

class Question(BaseModel):
    type: str
    question: str
    options: List[str] = []
    answer: str
    difficulty: str
    topic: str = "General"
   
class QuizRequest(BaseModel):
    goal: str
    num_questions: int
    difficulty: str
    topic: Optional[str] = None

class QuizResponse(BaseModel):
    quiz_id: str
    goal: str
    questions: List[Question]
    error: Optional[str] = None