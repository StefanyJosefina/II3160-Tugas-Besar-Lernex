from typing import Optional, List
from datetime import timedelta, datetime, timezone
from uuid import uuid4

from pydantic import BaseModel, Field


class CourseTopic(BaseModel):
    topic_id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    description: Optional[str] = None
    order: int
    estimated_duration_minutes: Optional[int] = None
    content_url: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CourseLesson(BaseModel):
    lesson_id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    description: Optional[str] = None
    order: int
    topics: List[CourseTopic] = Field(default_factory=list)
    estimated_duration_minutes: Optional[int] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CourseModule(BaseModel):
    module_id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    description: Optional[str] = None
    order: int
    lessons: List[CourseLesson] = Field(default_factory=list)
    estimated_duration_minutes: Optional[int] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))


class CourseDetail(BaseModel):
    duration: Optional[timedelta] = None
    level: Optional[str] = None
    category: Optional[str] = None
    total_modules: int = 0
    total_lessons: int = 0
    total_topics: int = 0


class Instructor(BaseModel):
    instructor_id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    bio: Optional[str] = None


class Course(BaseModel):
    course_id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    description: str
    instructor_id: str
    modules: List[CourseModule] = Field(default_factory=list)
    detail: Optional[CourseDetail] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))