from datetime import datetime
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class ProgressStatus(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    ON_HOLD = "ON_HOLD"


class LearningProgress(BaseModel):
    progress_id: str = Field(default_factory=lambda: str(uuid4()))
    learner_id: str
    course_id: str
    completion_rate: float = 0.0 
    last_accessed: datetime = Field(default_factory=datetime.utcnow)
    status: ProgressStatus = ProgressStatus.IN_PROGRESS