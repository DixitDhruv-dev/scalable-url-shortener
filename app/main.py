from fastapi import FastAPI

from app.api.routes.redirect import router as redirect_router
from app.api.routes.urls import router as urls_router
from app.core.config import get_settings


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
)


app.include_router(urls_router)
app.include_router(redirect_router)



@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "environment": settings.app_env,
    }