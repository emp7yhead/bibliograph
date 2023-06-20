from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.sentences.models import Sentence


async def add_sentence(session: AsyncSession, book_id: int, sentence: list):
    return await session.execute(
            insert(Sentence)
            .values(
                book_id=book_id,
                content=''.join(sentence))
            .returning(Sentence.id)
        )
