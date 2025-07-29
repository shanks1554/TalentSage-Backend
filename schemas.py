from pydantic import BaseModel
from typing import List

class EvaluationResult(BaseModel):
    fit_score: int
    strengths: List[str]
    weaknesses: List[str]
    recommendation: str
