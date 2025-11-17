from typing import Dict, List

from fastapi import APIRouter, HTTPException

from ..domain.enrollment import Enrollment

router = APIRouter(prefix="/enrollments", tags=["Enrollments"])

_enrollments: Dict[str, Enrollment] = {}


@router.post("/", response_model=Enrollment)
def create_enrollment(enrollment: Enrollment) -> Enrollment:
    if enrollment.enrollment_id in _enrollments:
        raise HTTPException(status_code=400, detail="Enrollment already exists")
    _enrollments[enrollment.enrollment_id] = enrollment
    return enrollment


@router.get("/", response_model=List[Enrollment])
def list_enrollments() -> List[Enrollment]:
    return list(_enrollments.values())


@router.get("/{enrollment_id}", response_model=Enrollment)
def get_enrollment(enrollment_id: str) -> Enrollment:
    enrollment = _enrollments.get(enrollment_id)
    if not enrollment:
        raise HTTPException(status_code=404, detail="Enrollment not found")
    return enrollment