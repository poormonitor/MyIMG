from functools import lru_cache

from pydantic import BaseSettings
import codecs
import os


class Settings(BaseSettings):
    DB_PATH: str = "sqlite:///data.sqlite"
    MYIMG_SECRET_KEY: str = codecs.encode(os.urandom(32), "hex").decode()
    S3_ENDPOINT: str = ""
    S3_SECRET_ID: str = ""
    S3_SECRET_KEY: str = ""
    S3_REGION: str = ""
    S3_BUCKET: str = ""
    S3_PREFIX: str = ""
    S3_DOMAIN_PREFIX: str = ""
    REGISTER: int = 1

    class Config:
        env_file = ".env"

    def __getitem__(self, item: str):
        return getattr(self, item)


def get_secret_key() -> str:
    return get_config()["MYIMG_SECRET_KEY"]


@lru_cache()
def get_config() -> BaseSettings:
    return Settings()
