from fastapi import FastAPI

from .api.learner_router import router as learner_router
from .api.course_router import router as course_router
from .api.enrollment_router import router as enrollment_router
from .api.learning_progress_router import router as learning_progress_router
from .api.feedback_router import router as feedback_router
from .api.recommendation_router import router as recommendation_router
from .api.learning_record_router import router as learning_record_router

app = FastAPI(
    title="Lernex API",
    description="API dasar untuk Lernex - Digital Learning Marketplace",
    version="0.1.0",
)

app.include_router(learner_router)
app.include_router(course_router)
app.include_router(enrollment_router)
app.include_router(learning_progress_router)
app.include_router(feedback_router)
app.include_router(recommendation_router)
app.include_router(learning_record_router)


@app.get("/")
def root():
    return {"message": "Lernex API is running"}