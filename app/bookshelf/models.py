import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.books.models import Book
from app.database import Base


class Bookshelf(Base):
    __tablename__ = 'bookshelves'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    title: Mapped[str]
    books: Mapped[list[Book] | None] = relationship(
        lazy='selectin',
    )
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
