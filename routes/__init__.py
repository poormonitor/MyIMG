from fastapi import FastAPI, Request
import time


def init_app_routes(app: FastAPI):
    from .upload import router as upload_router
    from .index import router as index_router
    from .register import router as register_router
    from .login import router as token_router
    from .fetch import router as fetch_router

    app.include_router(upload_router)
    app.include_router(index_router)
    app.include_router(register_router)
    app.include_router(token_router)
    app.include_router(fetch_router)

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["X-Process-Time"] = str(process_time)
        return response