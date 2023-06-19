import datetime
import enum

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ReadStatus(enum.Enum):
    ADDED = 'added'
    STARTED = 'started'
    IN_PROGRESS = 'in progress'
    FINISHED = 'finished'


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    bookshelf_id: Mapped[int] = mapped_column(
        ForeignKey('bookshelves.id', ondelete='CASCADE')
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey('authors.id')
    )
    author: Mapped['Author'] = relationship(
        back_populates='books',
        lazy='selectin',
    )
    title: Mapped[str]
    total_pages: Mapped[int]
    readed_pages: Mapped[int] = mapped_column(default=0)
    first_sentence: Mapped['Sentence'] = relationship(
        back_populates='books',
        lazy='selectin',
        cascade="all, delete-orphan",
    )
    status: Mapped[ReadStatus] = mapped_column(default=ReadStatus.ADDED)
    added_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    started_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True),
    )
    finished_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True),
    )


class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    books: Mapped[list[Book]] = relationship(
        back_populates='author',
        lazy='selectin',
    )
    name: Mapped[str]


class Sentence(Base):
    __tablename__ = 'sentences'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))
    books: Mapped['Book'] = relationship(
        back_populates='first_sentence',
        lazy='selectin',
    )
    content: Mapped[str]
