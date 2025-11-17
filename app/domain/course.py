from typing import Optional
from datetime import timedelta
from uuid import uuid4

from pydantic import BaseModel, Field


class CourseDetail(BaseModel):
    duration: Optional[timedelta] = None
    level: Optional[str] = None
    category: Optional[str] = None


class Instructor(BaseModel):
    instructor_id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    bio: Optional[str] = None


class Course(BaseModel):
    course_id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    description: str
    instructor_id: str
    detail: Optional[CourseDetail] = None