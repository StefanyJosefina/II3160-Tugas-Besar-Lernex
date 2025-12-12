from typing import Dict, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext

from ..domain.user import Learner
from ..storage import _learners

router = APIRouter(prefix="/learners", tags=["Learners"])

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LearnerCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


class LearnerResponse(BaseModel):
    learner_id: str
    name: str
    email: EmailStr
    join_date: str


@router.post("/", response_model=Dict)
def create_learner(learner_data: LearnerCreate) -> Dict:
    for learner in _learners.values():
        if learner.email == learner_data.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    password_hash = pwd_context.hash(learner_data.password)
    
    new_learner = Learner(
        name=learner_data.name,
        email=learner_data.email,
        password_hash=password_hash
    )
    
    _learners[new_learner.learner_id] = new_learner
    
    return {
        "learner_id": new_learner.learner_id,
        "name": new_learner.name,
        "email": new_learner.email,
        "join_date": new_learner.join_date,
        "message": "Learner created successfully"
    }


@router.get("/", response_model=List[Dict])
def list_learners() -> List[Dict]:
    return [
        {
            "learner_id": learner.learner_id,
            "name": learner.name,
            "email": learner.email,
            "join_date": learner.join_date,
        }
        for learner in _learners.values()
    ]


@router.get("/{learner_id}", response_model=Dict)
def get_learner(learner_id: str) -> Dict:
    learner = _learners.get(learner_id)
    if not learner:
        raise HTTPException(status_code=404, detail="Learner not found")
    return {
        "learner_id": learner.learner_id,
        "name": learner.name,
        "email": learner.email,
        "join_date": learner.join_date,
        "profile": learner.profile,
    }