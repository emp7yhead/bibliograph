import datetime
from time import timezone

from sqlalchemy import CheckConstraint, DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.bookshelf.models import Bookshelf
from app.database import Base


class ReadingSegment(Base):
    __tablename__ = 'reading_segments'
    __table_args__ = (
       CheckConstraint('started_at<finished_at')
    )

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    started_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
    )
    finished_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
    )
    readed_pages: Mapped[int]
    user_id: Mapped[int] = mapped_column('user.id')

    def __repr__(self):
        return f"<Segment({self.started_at} {self.finished_at} {self.readed_pages})>"
