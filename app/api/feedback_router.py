from typing import Dict, List

from fastapi import APIRouter, HTTPException

from ..domain.feedback import Feedback

router = APIRouter(prefix="/feedback", tags=["Feedback"])

_feedback_store: Dict[str, Feedback] = {}


@router.post("/", response_model=Feedback)
def create_feedback(feedback: Feedback) -> Feedback:
    if feedback.feedback_id in _feedback_store:
        raise HTTPException(status_code=400, detail="Feedback already exists")
    _feedback_store[feedback.feedback_id] = feedback
    return feedback


@router.get("/", response_model=List[Feedback])
def list_feedback() -> List[Feedback]:
    return list(_feedback_store.values())


@router.get("/{feedback_id}", response_model=Feedback)
def get_feedback(feedback_id: str) -> Feedback:
    feedback = _feedback_store.get(feedback_id)
    if not feedback:
        raise HTTPException(status_code=404, detail="Feedback not found")
    return feedback