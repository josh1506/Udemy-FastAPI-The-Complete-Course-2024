from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {"title": "Title 1", "author": "Author 1", "category": "Science"},
    {"title": "Title 2", "author": "Author", "category": "Science"},
    {"title": "Title 3", "author": "Author", "category": "Math"},
    {"title": "Title 4", "author": "Author 4", "category": "Math"},
]

@app.get("/books")
async def read_all_books():
    return BOOKS


@app.get("/books/{book_id}")
async def read_book(book_id: int):
    return BOOKS[book_id]


@app.get("/books/title/{book_title}")
async def read_book_title(book_title: str):
    for book in BOOKS:
        if book["title"].casefold() == book_title.casefold():
            return book


@app.get("/books/")
async def read_books_by_category(category: str):
    book_list = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            book_list.append(book)
    return book_list


@app.get("/books/author/{book_author}/")
async def read_books_by_author(book_author: str, category: str):
    book_list = []
    for book in BOOKS:
        is_book_author = book.get("author").casefold() == book_author.casefold()
        is_book_category = book.get("category").casefold() == category.casefold()
        if is_book_author and is_book_category:
            book_list.append(book)
    return book_list
