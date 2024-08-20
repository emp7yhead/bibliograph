from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.books.models import Book
from app.database import Base


class Sentence(Base):
    __tablename__ = 'sentences'

    id: Mapped[int] = mapped_column(
        primary_key=True, autoincrement=True, index=True,
    )
    book_id: Mapped[int] = mapped_column(
        ForeignKey('books.id', ondelete='CASCADE'),
    )
    books: Mapped['Book'] = relationship(
        back_populates='first_sentence',
        lazy='selectin',
    )
    content: Mapped[str]
