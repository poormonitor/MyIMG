from fastapi import APIRouter, Depends, Request, UploadFile
from typing import Optional
from pydantic import BaseModel, Field, validator
from models.pic import Pic
from models import get_db
from sqlalchemy.orm import Session
from auth import get_current_user
from s3 import get_presigned_post_url, put_object_s3
from uuid import uuid4
import os

router = APIRouter()


class requestUploadPost(BaseModel):
    file: UploadFile = Field(description="File to upload.")
    private: Optional[bool] = Field(
        description="Choose pic whether private or not. Default to false.",
        default=False,
    )


class responseUploadPost(BaseModel):
    pid: str = Field(description="The UUID for the picture. Useful so store it.")
    url: Optional[str] = Field(
        description="The URL to perform get picture. Available when it is public."
    )


class responseUrlUpload(BaseModel):
    url: str = Field(description="The Url to perform PUT request to.")
    pid: str = Field(description="The UUID for the picture. Useful so store it.")


class requestUrlUpload(BaseModel):
    ext: str = Field(
        description="The extension of the picture you want to upload.", example="png"
    )
    private: Optional[bool] = Field(
        description="Choose pic whether private or not. Default to false.",
        default=False,
    )

    @validator("ext")
    def ext_in_range(cls, ext):
        ALLOWED_EXT = [
            "xbm",
            "tif",
            "pjp",
            "svgz",
            "jpg",
            "jpeg",
            "ico",
            "tiff",
            "gif",
            "svg",
            "jfif",
            "webp",
            "png",
            "bmp",
            "pjpeg",
            "avif",
        ]

        if ext.lower() not in ALLOWED_EXT:
            raise ValueError("The extension is not allowed.")

        return ext


@router.post("/upload_url", response_model=responseUrlUpload)
def upload_url(
    request: Request,
    data: requestUrlUpload,
    db: Session = Depends(get_db),
    uid: str = Depends(get_current_user),
):
    pid = str(uuid4())
    url = get_presigned_post_url(data.ext, pid)
    new_pic = Pic(
        pid=pid,
        ext=data.ext,
        private=data.private,
        ip=request.client.host,
        owner_id=uid,
    )
    db.add(new_pic)
    db.commit()
    return responseUrlUpload(url=url, pid=pid)


@router.post("/upload", response_model=responseUploadPost)
def upload_post(
    request: Request,
    data: requestUploadPost,
    db: Session = Depends(get_db),
    uid: str = Depends(get_current_user),
):
    pid = str(uuid4())
    ext = os.path.splitext(data.file.filename)[1]
    key = pid + "." + ext

    pic = Pic(
        pid=pid, owner_id=uid, ext=ext, private=data.private, ip=request.client.host
    )
    db.add(pic)
    db.commit()

    url = put_object_s3(data.file, key)

    response = responseUploadPost(pid=pid)
    if not data.private:
        response.url = url

    return response
