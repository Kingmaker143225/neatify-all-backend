from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.router import router
from app.config.settings import settings


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    docs_url="/docs",
    redoc_url="/redoc",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # We'll lock this down in production.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(
    router,
    prefix="/api/v1",
)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Neatify Backend 🚀",
        "version": settings.app_version,
    }