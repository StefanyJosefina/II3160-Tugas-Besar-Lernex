from typing import Dict, List

from fastapi import APIRouter, HTTPException

from ..domain.recommendation import Recommendation

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

_recommendations: Dict[str, Recommendation] = {}


@router.post("/", response_model=Recommendation)
def create_recommendation(recommendation: Recommendation) -> Recommendation:
    if recommendation.recommendation_id in _recommendations:
        raise HTTPException(
            status_code=400, detail="Recommendation already exists"
        )
    _recommendations[recommendation.recommendation_id] = recommendation
    return recommendation


@router.get("/", response_model=List[Recommendation])
def list_recommendations() -> List[Recommendation]:
    return list(_recommendations.values())


@router.get("/{recommendation_id}", response_model=Recommendation)
def get_recommendation(recommendation_id: str) -> Recommendation:
    recommendation = _recommendations.get(recommendation_id)
    if not recommendation:
        raise HTTPException(status_code=404, detail="Recommendation not found")
    return recommendation