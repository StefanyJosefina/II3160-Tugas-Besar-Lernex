from typing import Dict, List

from fastapi import APIRouter, HTTPException, Depends

from ..domain.recommendation import Recommendation
from ..domain.user import Learner
from ..storage import _recommendations
from .auth_router import get_current_learner      

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])


@router.post("/", response_model=Recommendation)
def create_recommendation(
    recommendation: Recommendation,
    current_learner: Learner = Depends(get_current_learner)   
) -> Recommendation:
    if recommendation.recommendation_id in _recommendations:
        raise HTTPException(
            status_code=400, detail="Recommendation already exists"
        )
    _recommendations[recommendation.recommendation_id] = recommendation
    return recommendation


@router.get("/", response_model=List[Recommendation])
def list_recommendations(
    current_learner: Learner = Depends(get_current_learner)   
) -> List[Recommendation]:
    return list(_recommendations.values())


@router.get("/{recommendation_id}", response_model=Recommendation)
def get_recommendation(
    recommendation_id: str,
    current_learner: Learner = Depends(get_current_learner)  
) -> Recommendation:
    recommendation = _recommendations.get(recommendation_id)
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return recommendation