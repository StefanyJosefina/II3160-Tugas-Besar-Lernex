from typing import Dict, List

from fastapi import APIRouter, HTTPException

from ..domain.learning_progress import LearningProgress

router = APIRouter(prefix="/progress", tags=["Learning Progress"])

_progress_store: Dict[str, LearningProgress] = {}


@router.post("/", response_model=LearningProgress)
def create_progress(progress: LearningProgress) -> LearningProgress:
    if progress.progress_id in _progress_store:
        raise HTTPException(status_code=400, detail="Progress already exists")
    _progress_store[progress.progress_id] = progress
    return progress


@router.get("/", response_model=List[LearningProgress])
def list_progress() -> List[LearningProgress]:
    return list(_progress_store.values())


@router.get("/{progress_id}", response_model=LearningProgress)
def get_progress(progress_id: str) -> LearningProgress:
    progress = _progress_store.get(progress_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    return progress