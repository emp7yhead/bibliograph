from fastapi import APIRouter

from app.auth.routers import auth_router
from app.users.routers import user_router

main_router = APIRouter()

main_router.include_router(auth_router)
main_router.include_router(user_router)
