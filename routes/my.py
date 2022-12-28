from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from auth import get_current_user
from models import get_db
from models.pic import Pic
from s3 import delete_from_s3, get_final_url

router = APIRouter()


class ImageItem(BaseModel):
    pid: str = Field(description="The UUID of the image.")
    name: str= Field(description="The name of the image. Used to search.")
    url: str = Field(description="The URL to request.")
    indate: str = Field(description="The time of creating the image.")
    ext: str = Field(description="The extension of the image.")


class responseMyImage(BaseModel):
    list: List[ImageItem] = Field(
        description="List of the images for the current user."
    )


class requestDeleteImage(BaseModel):
    pid: str = Field(description="The UUID of the image to delete.")


@router.get("/my", response_model=responseMyImage, tags=["user"])
def my(uid: str = Depends(get_current_user), db: Session = Depends(get_db)):
    db.query(Pic).filter_by(owner_id=uid).filter_by(receipt=False).delete()
    db.commit()

    pics = db.query(Pic).filter_by(owner_id=uid).filter_by(receipt=True).all()

    rs = [
        ImageItem(
            pid=i.pid,
            url=get_final_url(i.pid, i.ext),
            name=i.name,
            ext=i.ext,
            indate=i.indate.strftime("%Y-%m-%d %H:%M:%S"),
        )
        for i in pics
    ]

    return responseMyImage(list=rs)


@router.post("/delete")
def delete(
    data: requestDeleteImage,
    uid: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    pic = db.query(Pic).filter_by(pid=data.pid).order_by(Pic.indate.desc()).first()
    if not pic:
        raise HTTPException(status_code=404, detail="The image not found.")
    if pic.owner_id != uid:
        raise HTTPException(
            status_code=403, detail="The owner of the image is not you."
        )

    delete_from_s3(pic.ext, pic.pid)

    db.delete(pic)
    db.commit()

    return {"result": "success"}
