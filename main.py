from fastapi import FastAPI

from routes import init_app_routes

from models import Base, engine
from meta import meta_tags, meta_description


app = FastAPI(
    title="MyIMG", version="0.1.0", openapi_tags=meta_tags, description=meta_description
)

init_app_routes(app)

Base.metadata.create_all(bind=engine)
