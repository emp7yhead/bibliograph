from datetime import datetime

from pydantic import BaseModel

from app.books.schemas import BookshelfBook


class BookshelfIn(BaseModel):
    title: str


class BookshelfOut(BookshelfIn):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class BookshelfOutDb(BookshelfOut):
    books: list[BookshelfBook]


class UserBookshelf(BookshelfIn):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True
