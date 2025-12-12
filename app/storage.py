from typing import Dict, Any
from datetime import datetime, timezone
from .domain.course import Course, CourseModule, CourseLesson, CourseTopic, CourseDetail

_learners: Dict[str, Any] = {}

_instructors: Dict[str, Any] = {
    "instr-001": {"instructor_id": "instr-001", "name": "John Doe", "bio": "Python expert"},
    "instr-002": {"instructor_id": "instr-002", "name": "Jane Smith", "bio": "FastAPI specialist"},
    "instr-003": {"instructor_id": "instr-003", "name": "Dr. Emily Chen", "bio": "Data Science researcher"},
}

_courses: Dict[str, Any] = {
    "course-001": Course(
        course_id="course-001",
        title="Python Fundamentals",
        description="Learn Python basics from scratch",
        instructor_id="instr-001",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        modules=[
            CourseModule(
                module_id="mod-001",
                title="Introduction to Python",
                description="Get started with Python",
                order=1,
                estimated_duration_minutes=120,
                lessons=[
                    CourseLesson(
                        lesson_id="les-001",
                        title="Variables and Data Types",
                        description="Learn about variables",
                        order=1,
                        estimated_duration_minutes=45,
                        topics=[
                            CourseTopic(
                                topic_id="top-001",
                                title="String Variables",
                                description="Understanding strings",
                                order=1,
                                content_url="https://example.com/strings",
                                estimated_duration_minutes=15
                            ),
                            CourseTopic(
                                topic_id="top-002",
                                title="Numeric Variables",
                                description="Understanding numbers",
                                order=2,
                                content_url="https://example.com/numbers",
                                estimated_duration_minutes=15
                            )
                        ]
                    )
                ]
            )
        ],
        detail=CourseDetail(total_modules=1, total_lessons=1, total_topics=2)
    ),
    "course-002": Course(
        course_id="course-002",
        title="Web Development with FastAPI",
        description="Build modern APIs with FastAPI",
        instructor_id="instr-002",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        modules=[
            CourseModule(
                module_id="mod-002",
                title="FastAPI Basics",
                description="FastAPI fundamentals",
                order=1,
                estimated_duration_minutes=150,
                lessons=[
                    CourseLesson(
                        lesson_id="les-002",
                        title="Creating Your First API",
                        description="Build a simple API",
                        order=1,
                        estimated_duration_minutes=60,
                        topics=[
                            CourseTopic(
                                topic_id="top-003",
                                title="HTTP Methods",
                                description="Understanding GET, POST, PUT, DELETE",
                                order=1,
                                content_url="https://example.com/http-methods",
                                estimated_duration_minutes=20
                            )
                        ]
                    )
                ]
            )
        ],
        detail=CourseDetail(total_modules=1, total_lessons=1, total_topics=1)
    ),
    "course-003": Course(
        course_id="course-003",
        title="Data Science Basics",
        description="Introduction to data science and analytics",
        instructor_id="instr-003",
        created_at=datetime.now(timezone.utc),
        updated_at=datetime.now(timezone.utc),
        modules=[
            CourseModule(
                module_id="mod-003",
                title="Data Analysis",
                description="Learn data analysis fundamentals",
                order=1,
                estimated_duration_minutes=180,
                lessons=[
                    CourseLesson(
                        lesson_id="les-003",
                        title="Working with Pandas",
                        description="Data manipulation with Pandas",
                        order=1,
                        estimated_duration_minutes=90,
                        topics=[
                            CourseTopic(
                                topic_id="top-004",
                                title="DataFrames",
                                description="Understanding DataFrames",
                                order=1,
                                content_url="https://example.com/dataframes",
                                estimated_duration_minutes=30
                            ),
                            CourseTopic(
                                topic_id="top-005",
                                title="Data Cleaning",
                                description="Cleaning and preparing data",
                                order=2,
                                content_url="https://example.com/cleaning",
                                estimated_duration_minutes=30
                            )
                        ]
                    )
                ]
            )
        ],
        detail=CourseDetail(total_modules=1, total_lessons=1, total_topics=2)
    )
}

_enrollments: Dict[str, Any] = {}
_feedback_store: Dict[str, Any] = {}
_progress_store: Dict[str, Any] = {}
_records: Dict[str, Any] = {}
_recommendations: Dict[str, Any] = {}