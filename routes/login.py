from pydantic import Field, BaseModel
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from auth import verify_passwd, create_access_token
from typing import Optional
from models.user import User
from models import get_db
from datetime import timedelta

router = APIRouter()


class requestUserLogin(BaseModel):
    email: str = Field(description="Email of the user.")
    password: str = Field(description="The password for the user.")
    expires: Optional[int] = Field(
        gt=0,
        lt=2592000,
        description="Time to expire the token. Default to 3600 seconds.",
        default=3600,
    )


class responseUserToken(BaseModel):
    access_token: str = Field(
        description="JWT Token for authorization. Store it and bear it when requesting."
    )
    token_type: str = "bearer"


@router.post("/login", response_model=responseUserToken)
def login(data: requestUserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=data.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found.")
    if not verify_passwd(data.password, user.passwd):
        raise HTTPException(status_code=400, detail="Password incorrect.")

    token = create_access_token(user.uid, timedelta(seconds=data.expires))

    return responseUserToken(access_token=token)


@router.post("/token", response_model=responseUserToken)
def token(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter_by(email=data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found.")
    if not verify_passwd(data.password, user.passwd):
        raise HTTPException(status_code=400, detail="Password incorrect.")

    token = create_access_token(user.uid, timedelta(seconds=3600))

    return responseUserToken(access_token=token)
