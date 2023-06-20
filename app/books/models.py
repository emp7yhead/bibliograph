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
        cascade="all, delete, delete-orphan",
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

    @property
    def progress(self):
        """Calculate reading progress."""
        return (self.total_pages / 100) * self.readed_pages

    @property
    def time_to_read(self):
        """Calculate total time to read book."""
        AVERAGE_PAGES_PER_HOUR = 50
        raw_time = round(self.total_pages / AVERAGE_PAGES_PER_HOUR, 2)
        hours: int = int(raw_time // 1)
        minutes: float = int(raw_time % 1 * 60)
        return f'{hours} hours {minutes} minutes'
