from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
import app.models  
from app.api.v1.api import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crea las tablas si no existen (ideal para dev rápido)
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "online",
        "project": settings.PROJECT_NAME,
        "version": settings.VERSION
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)