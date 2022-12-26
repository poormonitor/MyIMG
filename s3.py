from config import get_config
from minio import Minio
from datetime import timedelta
from fastapi import UploadFile, HTTPException

config = get_config()
minioClient = Minio(
    config["S3_ENDPOINT"],
    access_key=config["S3_SECRET_ID"],
    secret_key=config["S3_SECRET_KEY"],
    region=config["S3_REGION"],
    secure=True,
)


def get_presigned_post_url(ext: str, id: str) -> str:
    key = config["S3_PREFIX"] + "/" + id + "." + ext

    url = minioClient.presigned_put_object(
        config["S3_BUCKET"], key, expires=timedelta(hours=1)
    )

    return url


def get_presigned_get_url(key: str, expires: int = 3600) -> str:
    try:
        stat = minioClient.stat_object(config["S3_BUCKET"], key)
    except:
        raise HTTPException(status_code=400, detail="The file has not been uploaded.")

    from datetime import timedelta

    url = minioClient.presigned_get_object(
        config["S3_BUCKET"],
        config["S3_PREFIX"] + key,
        expires=timedelta(seconds=expires),
    )

    return url


def put_object_s3(data: UploadFile, key: str) -> str:
    try:
        minioClient.put_object(config["S3_BUCKET"], key, data, -1)
    except:
        raise HTTPException(status_code=400, detail="Error occurred during uploading.")

    return "https://" + config["S3_ENDPOINT"] + "/" + key