from datetime import datetime, timedelta
from typing import Optional, Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from pydantic import BaseModel

from ..domain.user import Learner
from .learner_router import _learners 

SECRET_KEY = "ganti_ini_dengan_secret_yang_lebih_sulit"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    learner_id: Optional[str] = None


router = APIRouter(prefix="/auth", tags=["Authentication"])


def create_access_token(
    data: Dict,
    expires_delta: Optional[timedelta] = None,
) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def authenticate_learner(email: str, password: str) -> Optional[Learner]:
    """
    Autentikasi sangat sederhana:
    cari learner berdasarkan email dan cek kecocokan password plain text.
    """
    for learner in _learners.values():
        if learner.email == email and learner.password == password:
            return learner
    return None


@router.post("/token", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    Endpoint login.
    username di form = email learner.
    """
    learner = authenticate_learner(form_data.username, form_data.password)
    if not learner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token({"sub": learner.learner_id})
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
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        learner_id: str = payload.get("sub")
        if learner_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    learner = _learners.get(learner_id)
    if learner is None:
        raise credentials_exception

    return learner