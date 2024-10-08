import datetime
import enum

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

AVERAGE_PAGES_PER_HOUR = 50


class ReadStatus(enum.Enum):
    ADDED = 'added'
    IN_PROGRESS = 'in progress'
    FINISHED = 'finished'


class Book(Base):
    __tablename__ = 'books'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True,
    )
    bookshelf_id: Mapped[int] = mapped_column(
        ForeignKey('bookshelves.id', ondelete='CASCADE'),
    )
    author_id: Mapped[int] = mapped_column(
        ForeignKey('authors.id'),
    )
    author: Mapped['Author'] = relationship(  # noqa: F821
        back_populates='books',
        lazy='selectin',
    )
    title: Mapped[str]
    total_pages: Mapped[int]
    readed_pages: Mapped[int] = mapped_column(default=0)
    first_sentence: Mapped['Sentence'] = relationship(  # noqa: F821
        back_populates='books',
        lazy='selectin',
        cascade='all, delete, delete-orphan',
    )
    status: Mapped[ReadStatus] = mapped_column(default=ReadStatus.ADDED)
    added_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True), server_default=func.now(),
    )
    started_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True),
    )
    finished_at: Mapped[datetime.datetime | None] = mapped_column(
        DateTime(timezone=True),
    )

    @property
    def reading_progress(self) -> str:
        """Calculate reading progress."""
        percentage = round(self.readed_pages / (self.total_pages / 100), 2)
        return f'{percentage}%'

    @property
    def time_to_read(self) -> str:
        """Calculate total time to read book."""

        raw_time = round(self.total_pages / AVERAGE_PAGES_PER_HOUR, 2)
        hours: int = int(raw_time // 1)
        minutes: float = int(raw_time % 1 * 60)
        return f'{hours} hours {minutes} minutes'
