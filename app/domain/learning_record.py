from typing import List
from uuid import uuid4

from pydantic import BaseModel, Field


class LearningRecord(BaseModel):
    record_id: str = Field(default_factory=lambda: str(uuid4()))
    learner_id: str
    completed_course_ids: List[str] = []
    ongoing_course_ids: List[str] = []
    enrollment_ids: List[str] = []