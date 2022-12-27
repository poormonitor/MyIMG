import os
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile
from pydantic import BaseModel, Field, validator
from sqlalchemy.orm import Session

from auth import get_current_user
from models import get_db
from models.pic import Pic
from s3 import get_presigned_post_url, put_object_s3

router = APIRouter()


class requestUploadReceipt(BaseModel):
    pid: str = Field(description="The UUID of the image to set be done.")


class requestUploadPost(BaseModel):
    file: UploadFile = Field(description="File to upload.")


class responseUploadPost(BaseModel):
    pid: str = Field(description="The UUID for the picture. Useful so store it.")
    url: str = Field(description="The URL to perform GET picture.")


class responseUrlUpload(BaseModel):
    url: str = Field(description="The URL to perform GET picture.")
    put: str = Field(description="The URL to perform POST request to. Use 'file' for form upload.")
    pid: str = Field(description="The UUID for the picture. Useful so store it.")
    key: str = Field(description="The key for S3 to write.")


class requestUrlUpload(BaseModel):
    ext: str = Field(
        description="The extension of the picture you want to upload.", example="png"
    )

    @validator("ext")
    def ext_in_range(cls, ext):
        from meta import ALLOWED_EXT

        if ext.lower() not in ALLOWED_EXT:
            raise ValueError("The extension is not allowed.")

        return ext


@router.post("/upload_url", response_model=responseUrlUpload, tags=["upload"])
def upload_url(
    request: Request,
    data: requestUrlUpload,
    db: Session = Depends(get_db),
    uid: str = Depends(get_current_user),
):
    pid = str(uuid4())
    put, url, key = get_presigned_post_url(data.ext, pid)
    new_pic = Pic(
        pid=pid,
        ext=data.ext,
        ip=request.client.host,
        owner_id=uid,
    )
    db.add(new_pic)
    db.commit()
    return responseUrlUpload(url=url, pid=pid, put=put, key=key)


@router.post("/upload", response_model=responseUploadPost, tags=["upload"])
def upload_post(
    request: Request,
    data: requestUploadPost,
    db: Session = Depends(get_db),
    uid: str = Depends(get_current_user),
):
    pid = str(uuid4())
    ext = os.path.splitext(data.file.filename)[1]
    key = pid + "." + ext

    pic = Pic(pid=pid, owner_id=uid, ext=ext, ip=request.client.host, receipt=True)
    db.add(pic)
    db.commit()

    url = put_object_s3(data.file, key)

    response = responseUploadPost(pid=pid, url=url)
    return response


@router.post("/receipt", tags=["upload"])
def receipt(
    data: requestUploadReceipt,
    uid: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    pic = db.query(Pic).filter_by(pid=data.pid).first()

    if not pic:
        raise HTTPException(status_code=400, detail="Image not found.")
    if pic.owner_id != uid:
        raise HTTPException(status_code=403, detail="The image not belongs to you.")

    pic.receipt = True
    db.commit()

    return {"result": "success"}
