from typing import Dict, List

from fastapi import APIRouter, HTTPException, Depends

from ..domain.learning_progress import LearningProgress
from ..domain.user import Learner
from ..storage import _progress_store
from .auth_router import get_current_learner     

router = APIRouter(prefix="/progress", tags=["Learning Progress"])


@router.post("/", response_model=LearningProgress)
def create_progress(
    progress: LearningProgress,
    current_learner: Learner = Depends(get_current_learner)  
) -> LearningProgress:
    if progress.progress_id in _progress_store:
        raise HTTPException(status_code=400, detail="Progress already exists")
    _progress_store[progress.progress_id] = progress
    return progress


@router.get("/", response_model=List[LearningProgress])
def list_progress(
    current_learner: Learner = Depends(get_current_learner)  
) -> List[LearningProgress]:
    return list(_progress_store.values())


@router.get("/{progress_id}", response_model=LearningProgress)
def get_progress(
    progress_id: str,
    current_learner: Learner = Depends(get_current_learner)   
) -> LearningProgress:
    progress = _progress_store.get(progress_id)
    if not progress:
        raise HTTPException(status_code=404, detail="Progress not found")
    return progress