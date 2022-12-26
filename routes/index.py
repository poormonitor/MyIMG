from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from pydantic import BaseModel

router = APIRouter()


@router.get("/")
def index():
    return RedirectResponse("/docs")
