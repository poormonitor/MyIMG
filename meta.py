meta_tags = [
    {
        "name": "upload",
        "description": "Upload the image. You can directly post it to the API or get POST URL of S3 and directly post to the provider.",
    },
    {
        "name": "user",
        "description": "Provide services like registering, login, changing password and managing images uploaded.",
    },
    {
        "name": "manage",
        "description": "Allow user to manage his/her images."
    }
    ,
    {
        "name": "admin",
        "description": "Administrator's management functions."
    }
]


meta_description = """
MyIMG builds a interface with S3 and common API to enhance experience when uploading a picture.
"""

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
