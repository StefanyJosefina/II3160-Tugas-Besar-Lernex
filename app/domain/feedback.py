from uuid import uuid4
from typing import Annotated
from pydantic import BaseModel, Field

RatingValue = Annotated[int, Field(ge=1, le=5)]

class Rating(BaseModel):
    value: RatingValue = 5
    comment_category: str = "general"


class Feedback(BaseModel):
    feedback_id: str = Field(default_factory=lambda: str(uuid4()))
    learner_id: str
    course_id: str
    comment: str
    rating: Rating