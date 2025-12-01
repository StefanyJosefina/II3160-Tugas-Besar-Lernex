from typing import Dict, List

from fastapi import APIRouter, HTTPException, Depends

from ..domain.feedback import Feedback
from ..domain.user import Learner
from .auth_router import get_current_learner   

router = APIRouter(prefix="/feedback", tags=["Feedback"])

_feedback_store: Dict[str, Feedback] = {}


@router.post("/", response_model=Feedback)
def create_feedback(
    feedback: Feedback,
    current_learner: Learner = Depends(get_current_learner)   
) -> Feedback:
    if feedback.feedback_id in _feedback_store:
        raise HTTPException(status_code=400, detail="Feedback already exists")
    _feedback_store[feedback.feedback_id] = feedback
    return feedback


@router.get("/", response_model=List[Feedback])
def list_feedback(
    current_learner: Learner = Depends(get_current_learner)   
) -> List[Feedback]:
    return list(_feedback_store.values())


@router.get("/{feedback_id}", response_model=Feedback)
def get_feedback(
    feedback_id: str,
    current_learner: Learner = Depends(get_current_learner)  
) -> Feedback:
    feedback = _feedback_store.get(feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback