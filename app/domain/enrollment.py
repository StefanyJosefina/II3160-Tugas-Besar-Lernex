from datetime import datetime
from enum import Enum
from uuid import uuid4

from pydantic import BaseModel, Field


class EnrollmentStatus(str, Enum):
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"


class Enrollment(BaseModel):
    enrollment_id: str = Field(default_factory=lambda: str(uuid4()))
    learner_id: str
    course_id: str
    enrollment_date: datetime = Field(default_factory=datetime.utcnow)
    status: EnrollmentStatus = EnrollmentStatus.ACTIVE