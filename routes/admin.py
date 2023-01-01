from fastapi import Depends, APIRouter
from pydantic import BaseModel
from auth import admin_required
from config import Settings, get_config
import dotenv

router = APIRouter()


class requestSetSettings(Settings, BaseModel):
    pass


@router.get("/admin/config", tags=["admin"])
def get_config(
    settings: Settings = Depends(get_config),
    _: bool = Depends(admin_required),
):
    return {"config": settings.dict()}


@router.post("/admin/setconfig", tags=["admin"])
def set_config(
    settings: requestSetSettings,
    _: bool = Depends(admin_required),
):
    dotenv_file = dotenv.find_dotenv()
    dotenv.load_dotenv(dotenv_file)
    for i in settings.dict().keys():
        dotenv.set_key(dotenv_file, i, str(settings[i]))
    return {"result": "success"}
