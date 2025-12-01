from typing import Dict, List

from fastapi import APIRouter, HTTPException, Depends

from ..domain.learning_record import LearningRecord
from ..domain.user import Learner
from .auth_router import get_current_learner     

router = APIRouter(prefix="/learning-records", tags=["Learning Records"])

_records: Dict[str, LearningRecord] = {}


@router.post("/", response_model=LearningRecord)
def create_record(
    record: LearningRecord,
    current_learner: Learner = Depends(get_current_learner) 
) -> LearningRecord:
    if record.record_id in _records:
        raise HTTPException(status_code=400, detail="Record already exists")
    _records[record.record_id] = record
    return record


@router.get("/", response_model=List[LearningRecord])
def list_records(
    current_learner: Learner = Depends(get_current_learner)   
) -> List[LearningRecord]:
    return list(_records.values())


@router.get("/{record_id}", response_model=LearningRecord)
def get_record(
    record_id: str,
    current_learner: Learner = Depends(get_current_learner)   
) -> LearningRecord:
    record = _records.get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")
    return record