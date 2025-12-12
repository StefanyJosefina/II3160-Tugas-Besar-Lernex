from datetime import datetime, timedelta, timezone
from typing import Optional, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from pydantic import BaseModel, EmailStr
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

from ..domain.user import Learner
from ..storage import _learners 

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

security = HTTPBearer()


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    learner_id: Optional[str] = None
    email: Optional[str] = None


class TokenPayload(BaseModel):
    sub: str
    email: str
    iat: datetime
    exp: datetime


class LearnerRegister(BaseModel):
    name: str
    email: EmailStr
    password: str


class LearnerRegisterResponse(BaseModel):
    learner_id: str
    name: str
    email: str
    message: str


class LearnerLogin(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    learner_id: str
    name: str
    email: str


router = APIRouter(prefix="/auth", tags=["Authentication"])


def verify_password(plain_password: str, password_hash: str) -> bool:
    return pwd_context.verify(plain_password, password_hash)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    data: Dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    to_encode = data.copy()
    now = datetime.now(timezone.utc)
    expire = now + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    to_encode.update({
        "iat": now,
        "exp": expire,
    })
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_learner(email: str, password: str) -> Optional[Learner]:
    for learner in _learners.values():
        if learner.email == email:
            if verify_password(password, learner.password_hash):
                return learner
    return None


@router.post("/register", response_model=LearnerRegisterResponse)
def register_learner(learner_data: LearnerRegister):
    for learner in _learners.values():
        if learner.email == learner_data.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    password_hash = get_password_hash(learner_data.password)
    
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
        "message": "Learner registered successfully. You can now login."
    }


@router.post("/login", response_model=LoginResponse)
def login(login_data: LearnerLogin):
    learner = authenticate_learner(login_data.email, login_data.password)
    if not learner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = create_access_token({
        "sub": learner.learner_id,
        "email": learner.email,
    })
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "learner_id": learner.learner_id,
        "name": learner.name,
        "email": learner.email,
    }


async def get_current_learner(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> Learner:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            credentials.credentials, 
            SECRET_KEY, 
            algorithms=[ALGORITHM]
        )
        learner_id: str = payload.get("sub")
        email: str = payload.get("email")
        
        if learner_id is None:
            raise credentials_exception
            
        token_data = TokenData(learner_id=learner_id, email=email)
        
    except JWTError:
        raise credentials_exception

    learner = _learners.get(token_data.learner_id)
    if learner is None:
        raise credentials_exception

    return learner


@router.get("/me", response_model=Dict)
async def get_current_user(
    current_learner: Learner = Depends(get_current_learner)
):
    return {
        "learner_id": current_learner.learner_id,
        "name": current_learner.name,
        "email": current_learner.email,
        "join_date": current_learner.join_date,
    }