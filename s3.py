from datetime import timedelta

from fastapi import HTTPException, UploadFile
from minio import Minio

from config import get_config

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

    url = minioClient.get_presigned_url(
        "POST", config["S3_BUCKET"], key, expires=timedelta(hours=1)
    )

    if config["S3_DOMAIN_PREFIX"]:
        final_url = config["S3_DOMAIN_PREFIX"] + "/" + key
    else:
        final_url = "https://" + config["S3_ENDPOINT"] + "/" + key

    return url, final_url, key


def put_object_s3(data: UploadFile, key: str) -> str:
    try:
        minioClient.put_object(config["S3_BUCKET"], key, data, -1)
    except:
        raise HTTPException(status_code=400, detail="Error occurred during uploading.")

    return "https://" + config["S3_ENDPOINT"] + "/" + key


def delete_from_s3(ext: str, pid: str):
    key = config["S3_PREFIX"] + "/" + pid + "." + ext
    minioClient.remove_object(config["S3_BUCKET"], key)


def get_final_url(pid: str, ext: str):
    key = config["S3_PREFIX"] + "/" + pid + "." + ext

    if config["S3_DOMAIN_PREFIX"]:
        final_url = config["S3_DOMAIN_PREFIX"] + "/" + key
    else:
        final_url = "https://" + config["S3_ENDPOINT"] + "/" + key
    
    return final_url