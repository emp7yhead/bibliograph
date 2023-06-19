from datetime import datetime

from pydantic import BaseModel, EmailStr, Field

from app.bookshelf.schemas import UserBookshelf


class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(max_length=50)


class UserIn(UserBase):
    password: str = Field(min_length=3, max_length=50)


class UserOut(UserBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserOutDb(UserOut):
    bookshelves: list[UserBookshelf] | None
