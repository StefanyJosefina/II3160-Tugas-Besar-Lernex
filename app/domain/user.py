from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, EmailStr, Field
from uuid import uuid4


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
    join_date: datetime = Field(default_factory=datetime.utcnow)
    profile: Optional[Profile] = None