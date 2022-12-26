from fastapi import APIRouter, Depends, HTTPException
from models import get_db
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from models.user import User
from auth import hash_passwd

router = APIRouter()


class requestUserRegister(BaseModel):
    email: str = Field(
        regex=r"^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$",
        example="test@example.com",
    )
    passwd: str = Field(
        regex=r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$",
        description="The password must include digits, alphabets and is not shorter than 8 characters.",
    )


@router.post("/register")
def register(data: requestUserRegister, db: Session = Depends(get_db)):
    current = db.query(User).filter_by(email=data.email).count()
    if current > 0:
        raise HTTPException(status_code=400, detail="The email exists.")
    hashed = hash_passwd(data.passwd)
    new_user = User(email=data.email, passwd=hashed)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return {"result": "success"}
