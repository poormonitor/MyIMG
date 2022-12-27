import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles


def init_app_routes(app: FastAPI):
    from .login import router as token_router
    from .my import router as my_router
    from .register import router as register_router
    from .upload import router as upload_router

    app.include_router(upload_router, prefix="/api")
    app.include_router(register_router, prefix="/api")
    app.include_router(token_router, prefix="/api")
    app.include_router(my_router, prefix="/api")

    @app.get("/")
    def index():
        return FileResponse(path="view/dist/index.html")

    app.mount("/", StaticFiles(directory="view/dist"), name="static")

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response

    @app.middleware("http")
    async def add_cache_control(request: Request, call_next):
        response = await call_next(request)
        if "Cache-Control" not in response.headers:
            for tp in ["image", "font", "css", "javascript"]:
                if tp in response.headers["Content-Type"]:
                    response.headers["Cache-Control"] = "public, max-age=2592000"
                    break
            else:
                response.headers["Cache-Control"] = "no-store"
        return response

    app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
