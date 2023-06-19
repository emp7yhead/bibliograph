from fastapi import APIRouter

from app.auth.routers import auth_router
from app.books.routers import books_router
from app.bookshelf.routers import bookshelf_router
from app.users.routers import user_router

main_router = APIRouter()

main_router.include_router(auth_router)
main_router.include_router(user_router)
main_router.include_router(bookshelf_router)
main_router.include_router(books_router)
