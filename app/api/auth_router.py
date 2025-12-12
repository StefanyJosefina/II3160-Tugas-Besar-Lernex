from datetime import datetime, timedelta
from typing import Optional, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

from ..domain.user import Learner
from .learner_router import _learners 

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "your-super-secret-key-change-this-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


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
    now = datetime.utcnow()
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


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    learner = authenticate_learner(form_data.username, form_data.password)
    if not learner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({
        "sub": learner.learner_id,
        "email": learner.email,
    })
    return {"access_token": access_token, "token_type": "bearer"}


async def get_current_learner(
    token: str = Depends(oauth2_scheme),
) -> Learner:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, 
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