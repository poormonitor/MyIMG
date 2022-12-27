from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from auth import get_current_user, hash_passwd, verify_passwd
from models import get_db
from models.user import User

router = APIRouter()


class requestUserRegister(BaseModel):
    email: str = Field(
        regex=r"^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$",
        example="test@example.com",
    )
    password: str = Field(
        regex=r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
        description="The password must include digits, alphabets and is not shorter than 8 characters.",
    )


class requestUserPasswd(BaseModel):
    old: str = Field(description="Origin Password.")
    new: str = Field(
        regex=r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
        description="New Password. The password must include digits, alphabets and is not shorter than 8 characters.",
    )


@router.post("/register", tags=["user"])
def register(data: requestUserRegister, db: Session = Depends(get_db)):
    current = db.query(User).filter_by(email=data.email).count()
    if current > 0:
        raise HTTPException(status_code=400, detail="The email exists.")
    hashed = hash_passwd(data.password)
    new_user = User(email=data.email, passwd=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"result": "success"}


@router.post("/passwd", tags=["user"])
def passwd(
    data: requestUserPasswd,
    db: Session = Depends(get_db),
    uid: str = Depends(get_current_user),
):
    user = db.query(User).filter_by(uid=uid).first()
    
    if not verify_passwd(data.old, user.passwd):
        raise HTTPException(status_code=400, detail="The origin password is incorrect.")

    user.passwd = hash_passwd(data.new)
    db.commit()

    return {"result": "success"}
