from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import Field, BaseModel
from models.pic import Pic
from models import get_db
from sqlalchemy.orm import Session
from s3 import get_presigned_get_url
from auth import get_current_user

router = APIRouter()


class responseFetch(BaseModel):
    url: str = Field(description="Actual URL to request, which has been signed.")


class requestFetch(BaseModel):
    pid: str = Field(description="The UUID for the picture.")


@router.get("/fetch", response_model=responseFetch, tags=["fetch"])
def fetch(data: requestFetch, db: Session = Depends(get_db)):
    pic = db.query(Pic).filter_by(pid=data.pid).first()
    if not pic:
        raise HTTPException(status_code=404, detail="Picture not found.")
    if pic.private:
        get_current_user()

    url = get_presigned_get_url(pic.pid + "." + pic.ext)

    return responseFetch(url=url)


@router.get("/redirect", tags=["redirect"])
def redirect(data: requestFetch, db: Session = Depends(get_db)):
    pic = db.query(Pic).filter_by(pid=data.pid).first()
    if not pic:
        raise HTTPException(status_code=404, detail="Picture not found.")
    if pic.private:
        get_current_user()

    url = get_presigned_get_url(pic.pid + "." + pic.ext)

    return RedirectResponse(url=url)
