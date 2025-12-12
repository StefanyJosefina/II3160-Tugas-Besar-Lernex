from typing import Dict, List

from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel

from ..domain.course import Course
from ..domain.user import Learner
from ..storage import _courses, _enrollments, _instructors
from .auth_router import get_current_learner   


class CourseListResponse(BaseModel):
    course_id: str
    title: str
    description: str
    instructor_id: str
    instructor_name: str
    total_modules: int
    total_lessons: int
    total_topics: int


class EnrollResponse(BaseModel):
    message: str
    enrollment_id: str
    course_id: str
    learner_id: str


class EnrolledCourseResponse(BaseModel):
    enrollment_id: str
    course_id: str
    title: str
    description: str
    instructor_id: str
    instructor_name: str
    enrolled_at: str
    total_modules: int
    total_lessons: int
    total_topics: int


router = APIRouter(prefix="/courses", tags=["Courses"])


@router.get("/", response_model=List[CourseListResponse])
def list_courses(
    current_learner: Learner = Depends(get_current_learner)
) -> List[CourseListResponse]:
    """List all available courses for learner to explore and enroll"""
    courses = []
    for course in _courses.values():
        instructor = _instructors.get(course.instructor_id, {})
        courses.append(
            CourseListResponse(
                course_id=course.course_id,
                title=course.title,
                description=course.description,
                instructor_id=course.instructor_id,
                instructor_name=instructor.get("name", "Unknown"),
                total_modules=len(course.modules),
                total_lessons=sum(len(m.lessons) for m in course.modules),
                total_topics=sum(len(l.topics) for m in course.modules for l in m.lessons)
            )
        )
    return courses

@router.get("/my-courses", response_model=List[EnrolledCourseResponse])
def get_my_courses(
    current_learner: Learner = Depends(get_current_learner)
) -> List[EnrolledCourseResponse]:
    """Get all courses that learner has enrolled in"""
    my_courses = []
    
    for enrollment in _enrollments.values():
        if enrollment.get("learner_id") == current_learner.learner_id:
            course_id = enrollment.get("course_id")
            course = _courses.get(course_id)
            if course:
                instructor = _instructors.get(course.instructor_id, {})
                my_courses.append(
                    EnrolledCourseResponse(
                        enrollment_id=enrollment.get("enrollment_id"),
                        course_id=course.course_id,
                        title=course.title,
                        description=course.description,
                        instructor_id=course.instructor_id,
                        instructor_name=instructor.get("name", "Unknown"),
                        enrolled_at=enrollment.get("enrolled_at"),
                        total_modules=len(course.modules),
                        total_lessons=sum(len(m.lessons) for m in course.modules),
                        total_topics=sum(len(l.topics) for m in course.modules for l in m.lessons)
                    )
                )
    
    return my_courses


@router.get("/{course_id}", response_model=Course)
def get_course_detail(
    course_id: str,
    current_learner: Learner = Depends(get_current_learner)
) -> Course:
    """Get detailed course structure including all modules, lessons, and topics"""
    course = _courses.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@router.post("/{course_id}/enroll", response_model=EnrollResponse)
def enroll_course(
    course_id: str,
    current_learner: Learner = Depends(get_current_learner)
) -> EnrollResponse:
    """Enroll learner to a course"""
    course = _courses.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    enrollment_id = f"{current_learner.learner_id}-{course_id}"
    if enrollment_id in _enrollments:
        raise HTTPException(status_code=400, detail="Already enrolled in this course")
    
    _enrollments[enrollment_id] = {
        "enrollment_id": enrollment_id,
        "learner_id": current_learner.learner_id,
        "course_id": course_id,
        "enrolled_at": str(__import__('datetime').datetime.utcnow())
    }
    
    return EnrollResponse(
        message="Successfully enrolled in course",
        enrollment_id=enrollment_id,
        course_id=course_id,
        learner_id=current_learner.learner_id
    )