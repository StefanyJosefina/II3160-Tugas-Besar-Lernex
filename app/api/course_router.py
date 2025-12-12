from typing import Dict, List, Optional

from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Response, status
from pydantic import BaseModel

from ..domain.course import Course, CourseModule, CourseLesson, CourseTopic, CourseDetail
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


@router.post("/{course_id}/modules", response_model=CourseModule)
def add_module_to_course(
    course_id: str,
    module: CourseModule,
    current_learner: Learner = Depends(get_current_learner)
) -> CourseModule:
    course = _courses.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    course.modules.append(module)
    total_modules = len(course.modules)
    total_lessons = sum(len(m.lessons) for m in course.modules)
    total_topics = sum(len(l.topics) for m in course.modules for l in m.lessons)
    if course.detail:
        course.detail.total_modules = total_modules
        course.detail.total_lessons = total_lessons
        course.detail.total_topics = total_topics
    else:
        course.detail = CourseDetail(total_modules=total_modules, total_lessons=total_lessons, total_topics=total_topics)
    course.updated_at = datetime.utcnow()
    return module


@router.get("/{course_id}/modules", response_model=List[CourseModule])
def get_course_modules(
    course_id: str,
    current_learner: Learner = Depends(get_current_learner)
) -> List[CourseModule]:
    course = _courses.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    return course.modules


class ModuleUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    order: Optional[int] = None
    estimated_duration_minutes: Optional[int] = None


@router.put("/{course_id}/modules/{module_id}", response_model=CourseModule)
def update_module(
    course_id: str,
    module_id: str,
    update: ModuleUpdate,
    current_learner: Learner = Depends(get_current_learner),
) -> CourseModule:
    course = _courses.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    module = next((m for m in course.modules if m.module_id == module_id), None)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    if update.title is not None:
        module.title = update.title
    if update.description is not None:
        module.description = update.description
    if update.order is not None:
        module.order = update.order
    if update.estimated_duration_minutes is not None:
        module.estimated_duration_minutes = update.estimated_duration_minutes

    course.updated_at = datetime.utcnow()

    return module


@router.post("/{course_id}/modules/{module_id}/lessons", response_model=CourseLesson)
def add_lesson_to_module(
    course_id: str,
    module_id: str,
    lesson: CourseLesson,
    current_learner: Learner = Depends(get_current_learner)
) -> CourseLesson:
    course = _courses.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    module = next((m for m in course.modules if m.module_id == module_id), None)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    module.lessons.append(lesson)
    total_lessons = sum(len(m.lessons) for m in course.modules)
    total_topics = sum(len(l.topics) for m in course.modules for l in m.lessons)
    if course.detail:
        course.detail.total_lessons = total_lessons
        course.detail.total_topics = total_topics
    else:
        course.detail = CourseDetail(total_modules=len(course.modules), total_lessons=total_lessons, total_topics=total_topics)
    course.updated_at = datetime.utcnow()
    return lesson


@router.get("/{course_id}/modules/{module_id}/lessons", response_model=List[CourseLesson])
def get_module_lessons(
    course_id: str,
    module_id: str,
    current_learner: Learner = Depends(get_current_learner)
) -> List[CourseLesson]:
    course = _courses.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    module = next((m for m in course.modules if m.module_id == module_id), None)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    return module.lessons


@router.post("/{course_id}/modules/{module_id}/lessons/{lesson_id}/topics", response_model=CourseTopic)
def add_topic_to_lesson(
    course_id: str,
    module_id: str,
    lesson_id: str,
    topic: CourseTopic,
    current_learner: Learner = Depends(get_current_learner)
) -> CourseTopic:
    course = _courses.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    module = next((m for m in course.modules if m.module_id == module_id), None)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    lesson = next((l for l in module.lessons if l.lesson_id == lesson_id), None)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    lesson.topics.append(topic)
    total_topics = sum(len(l.topics) for m in course.modules for l in m.lessons)
    if course.detail:
        course.detail.total_topics = total_topics
    else:
        course.detail = CourseDetail(total_modules=len(course.modules), total_lessons=sum(len(m.lessons) for m in course.modules), total_topics=total_topics)
    course.updated_at = datetime.utcnow()
    return topic


@router.get("/{course_id}/modules/{module_id}/lessons/{lesson_id}/topics", response_model=List[CourseTopic])
def get_lesson_topics(
    course_id: str,
    module_id: str,
    lesson_id: str,
    current_learner: Learner = Depends(get_current_learner)
) -> List[CourseTopic]:
    course = _courses.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    module = next((m for m in course.modules if m.module_id == module_id), None)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")
    
    lesson = next((l for l in module.lessons if l.lesson_id == lesson_id), None)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")
    
    return lesson.topics


@router.delete("/{course_id}/modules/{module_id}/lessons/{lesson_id}/topics/{topic_id}")
def delete_topic(
    course_id: str,
    module_id: str,
    lesson_id: str,
    topic_id: str,
    current_learner: Learner = Depends(get_current_learner)
 ) -> Response:
    course = _courses.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")

    module = next((m for m in course.modules if m.module_id == module_id), None)
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    lesson = next((l for l in module.lessons if l.lesson_id == lesson_id), None)
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    topic = next((t for t in lesson.topics if t.topic_id == topic_id), None)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")

    lesson.topics = [t for t in lesson.topics if t.topic_id != topic_id]
    total_topics = sum(len(l.topics) for m in course.modules for l in m.lessons)
    if course.detail:
        course.detail.total_topics = total_topics
    course.updated_at = datetime.utcnow()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/{course_id}/structure", response_model=Dict)
def get_course_structure(
    course_id: str,
    current_learner: Learner = Depends(get_current_learner)
) -> Dict:
    course = _courses.get(course_id)
    if not course:
        raise HTTPException(status_code=404, detail="Course not found")
    
    total_topics = sum(
        len(lesson.topics) 
        for module in course.modules 
        for lesson in module.lessons
    )
    
    return {
        "course_id": course.course_id,
        "title": course.title,
        "total_modules": len(course.modules),
        "total_lessons": sum(len(m.lessons) for m in course.modules),
        "total_topics": total_topics,
        "modules": course.modules
    }