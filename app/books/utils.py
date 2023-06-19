from typing import Any
import aiohttp

from app.books.schemas import BookForDb


def normalize(book_title: str):
    """Normalize title of book for request.

    Args:
        title: book title

    Returns: str
    """
    return book_title.replace(' ', '+')


async def get_raw_info(book_title: str) -> dict[str, Any]:
    """
    Get book info from openlibrary.org.

    Args:
        title: book title

    Returns: dict[str, Any]
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'https://openlibrary.org/search.json?q={book_title}&fields=number_of_pages_median,author_name,first_sentence,title&limit=1'  # noqa: E501
        ) as response:
            raw_info = await response.json()
    return raw_info['docs'][0]


async def get_book_info(book_title: str) -> BookForDb:
    """Pipeline for getting book info

    Args:
        book_title: book title

    Returns: BookForDb
    """
    normalized_title: str = normalize(book_title)
    raw_info: dict[str, Any] = await get_raw_info(normalized_title)
    return BookForDb.parse_obj(raw_info)
