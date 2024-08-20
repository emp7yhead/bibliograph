from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.books.models import Book
from app.database import Base


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True,
    )
    books: Mapped[list[Book]] = relationship(
        back_populates='author',
        lazy='selectin',
    )
    name: Mapped[str]
