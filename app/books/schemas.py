from datetime import datetime

from pydantic import BaseModel, Field

from app.books.models import ReadStatus


class Author(BaseModel):
    name: str

    class Config:
        orm_mode = True


class Sentence(BaseModel):
    content: str

    class Config:
        orm_mode = True


class BookIn(BaseModel):
    bookshelf_id: int
    title: str


class BookForDb(BaseModel):
    title: str
    total_pages: int = Field(alias='number_of_pages_median')
    author: list = Field(alias='author_name')
    first_sentence: list

    class Config:
        extra = 'ignore'


class BookOut(BookIn):
    id: int
    total_pages: str
    author: list[Author] | Author
    first_sentence: Sentence | None
    status: ReadStatus
    added_at: datetime | None

    class Config:
        orm_mode = True


class BookOutDb(BookOut):
    readed_pages: int
    started_at: datetime | None
    finished_at: datetime | None


class BookshelfBook(BaseModel):
    id: int
    title: str
    total_pages: str
    readed_pages: int
    status: ReadStatus
    added_at: datetime | None
    started_at: datetime | None
    finished_at: datetime | None

    class Config:
        orm_mode = True
