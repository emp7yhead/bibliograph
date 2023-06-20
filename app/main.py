from fastapi import FastAPI

from app.routers import main_router
from app.settings import settings

app = FastAPI(
    title=settings.app_name,
    description=settings.description,
    version=settings.version,
    contact=settings.contact,
    openapi_tags=settings.tags_metadata,
)

app.include_router(main_router)


@app.get('/')
def index() -> str:
    return 'Welcome to Bibliograph. Please go to /docs for more information.'


@app.get('/ping')
def ping() -> str:
    return 'pong'
