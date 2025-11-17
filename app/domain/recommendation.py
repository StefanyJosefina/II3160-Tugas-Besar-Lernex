from datetime import datetime
from typing import List
from uuid import uuid4

from pydantic import BaseModel, Field


class Recommendation(BaseModel):
    recommendation_id: str = Field(default_factory=lambda: str(uuid4()))
    learner_id: str
    course_ids: List[str] = []
    generated_date: datetime = Field(default_factory=datetime.utcnow)