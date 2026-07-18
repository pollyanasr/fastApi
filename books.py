from itertools import count
from typing import Annotated

from fastapi import FastAPI, HTTPException, Path, Query, status
from pydantic import BaseModel, Field

app = FastAPI(title="Books API")


class BookRequest(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    author: str = Field(min_length=1, max_length=120)
    category: str = Field(min_length=1, max_length=60)


class Book(BookRequest):
    id: int


_next_id = count(1)

BOOKS: list[Book] = [
    Book(id=next(_next_id), title='Title One', author='Author One', category='science'),
    Book(id=next(_next_id), title='Title Two', author='Author Two', category='science'),
    Book(id=next(_next_id), title='Title Three', author='Author Three', category='history'),
    Book(id=next(_next_id), title='Title Four', author='Author Four', category='math'),
    Book(id=next(_next_id), title='Title Five', author='Author Five', category='math'),
    Book(id=next(_next_id), title='Title Six', author='Author Two', category='math'),
]


def _matches(value: str, expected: str | None) -> bool:
    return expected is None or value.casefold() == expected.casefold()


def _find_index(book_id: int) -> int | None:
    return next(
        (i for i, book in enumerate(BOOKS) if book.id == book_id),
        None,
    )


def _get_index_or_404(book_id: int) -> int:
    index = _find_index(book_id)
    if index is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with id {book_id} not found",
        )
    return index


BookId = Annotated[int, Path(ge=1)]


@app.get("/books", response_model=list[Book])
async def read_all_books(
    title: Annotated[str | None, Query(max_length=120)] = None,
    author: Annotated[str | None, Query(max_length=120)] = None,
    category: Annotated[str | None, Query(max_length=60)] = None,
):
    return [
        book
        for book in BOOKS
        if _matches(book.title, title)
        and _matches(book.author, author)
        and _matches(book.category, category)
    ]


@app.post("/books", response_model=Book, status_code=status.HTTP_201_CREATED)
async def create_book(new_book: BookRequest):
    book = Book(id=next(_next_id), **new_book.model_dump())
    BOOKS.append(book)
    return book


@app.get("/books/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def read_book(book_id: BookId):
    return BOOKS[_get_index_or_404(book_id)]


@app.put("/books/{book_id}", response_model=Book, status_code=status.HTTP_200_OK)
async def update_book(book_id: BookId, updated_book: BookRequest):
    index = _get_index_or_404(book_id)
    book = Book(id=book_id, **updated_book.model_dump())
    BOOKS[index] = book
    return book


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: BookId):
    BOOKS.pop(_get_index_or_404(book_id))
