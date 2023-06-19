import datetime

from sqlalchemy import DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.bookshelf.models import Bookshelf
from app.database import Base


class User(Base):
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint('username'),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True
    )
    username: Mapped[str]
    email: Mapped[str] = mapped_column(index=True)
    password: Mapped[str]
    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    bookshelves: Mapped[Bookshelf | None] = relationship(
        cascade="all, delete-orphan",
        lazy='selectin',
    )

    def __repr__(self):
        return f"<User({self.username} {self.id} {self.email})>"
