from datetime import datetime, timezone
from typing import List, Optional
from uuid import uuid4

from pydantic import BaseModel, EmailStr, Field


class PreferenceProfile(BaseModel):
    interests: List[str] = []
    preferred_category: Optional[str] = None


class Profile(BaseModel):
    profile_id: str = Field(default_factory=lambda: str(uuid4()))
    preferences: PreferenceProfile = Field(default_factory=PreferenceProfile)
    last_login: Optional[datetime] = None


class AuthenticationCredential(BaseModel):
    email: EmailStr
    password_hash: str


class Learner(BaseModel):
    learner_id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    email: EmailStr
    password_hash: str 
    join_date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    profile: Optional[Profile] = None