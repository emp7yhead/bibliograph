from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import main_router
from app.settings import settings

app = FastAPI(
    title=settings.app_name,
    description=settings.description,
    version=settings.version,
    contact=settings.contact,
    openapi_tags=settings.tags_metadata,
)

origins = [
    "http://localhost:3000",
    "localhost:3000"
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


app.include_router(main_router)


@app.get('/')
def index() -> str:
    return 'Welcome to Bibliograph. Please go to /docs for more information.'


@app.get('/ping')
def ping() -> str:
    return 'pong'
