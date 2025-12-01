from typing import Dict, List

from fastapi import APIRouter, HTTPException, Depends

from ..domain.course import Course
from ..domain.user import Learner
from .auth_router import get_current_learner   

router = APIRouter(prefix="/courses", tags=["Courses"])

_courses: Dict[str, Course] = {}


@router.post("/", response_model=Course)
def create_course(
    course: Course,
    current_learner: Learner = Depends(get_current_learner)   
) -> Course:
    if course.course_id in _courses:
        raise HTTPException(status_code=400, detail="Course already exists")
    _courses[course.course_id] = course
    return course


@router.get("/", response_model=List[Course])
def list_courses(
    current_learner: Learner = Depends(get_current_learner)   
) -> List[Course]:
    return list(_courses.values())


@router.get("/{course_id}", response_model=Course)
def get_course(
    course_id: str,
    current_learner: Learner = Depends(get_current_learner)   
) -> Course:
    course = _courses.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course