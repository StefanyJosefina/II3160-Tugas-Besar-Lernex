from typing import Dict, List

from fastapi import APIRouter, HTTPException

from ..domain.user import Learner

router = APIRouter(prefix="/learners", tags=["Learners"])

_learners: Dict[str, Learner] = {}


@router.post("/", response_model=Learner)
def create_learner(learner: Learner) -> Learner:
    if learner.learner_id in _learners:
        raise HTTPException(status_code=400, detail="Learner already exists")
    _learners[learner.learner_id] = learner
    return learner


@router.get("/", response_model=List[Learner])
def list_learners() -> List[Learner]:
    return list(_learners.values())


@router.get("/{learner_id}", response_model=Learner)
def get_learner(learner_id: str) -> Learner:
    learner = _learners.get(learner_id)
    if not learner:
        raise HTTPException(status_code=404, detail="Learner not found")
    return learner