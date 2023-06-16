import datetime

from sqlalchemy import DateTime, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

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

    def __repr__(self):
        return f"<User({self.username} {self.id} {self.email})>"
