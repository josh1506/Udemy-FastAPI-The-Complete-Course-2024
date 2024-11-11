from typing import Optional

from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3, max_length=50)
    author: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(ge=0, le=5)
    published_date: int = Field(ge=1999, lt=2031)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Mark cowell",
                "description": "A new description of the book",
                "rating": 3,
                "published_date": 2019
            }
        }
    }


BOOKS = [
    Book(1, "Computer Science Pro", "Jack Milter", "A very nice book!", 5, 2020),
    Book(2, "Python Essentials", "Laura Smith", "Comprehensive guide to Python.", 4, 2023),
    Book(3, "Advanced Django", "Megan Lee", "For Django enthusiasts.", 5, 2021),
    Book(4, "Data Science Handbook", "Alan Turing", "Deep dive into data science.", 5, 2020),
    Book(5, "Machine Learning Basics", "Tom Hawk", "Fundamentals of ML.", 4, 2023),
    Book(6, "Deep Learning Mastery", "Anna Bishop", "Insight into deep learning.", 5, 2022),
    Book(7, "Artificial Intelligence Primer", "John Doe", "Introduction to AI.", 4, 2021),
    Book(8, "React for Beginners", "Chris Pine", "Getting started with React.", 4, 2020),
    Book(9, "JavaScript Essentials", "Dana White", "JavaScript fundamentals.", 3, 2022),
    Book(10, "Cloud Computing Guide", "Sarah Connor", "Overview of cloud computing.", 4, 2023),
]


@app.get("/books")
async def get_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
async def get_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.get("/books/", status_code=status.HTTP_200_OK)
async def read_book_by_rating(book_rating: int = Query(ge=0, le=5)):
    book_list = []
    for book in BOOKS:
        if book_rating == book.rating:
            book_list.append(book)
    return book_list


@app.post("/books", status_code=status.HTTP_201_CREATED)
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_by_id(new_book))


@app.get("/books/published/", status_code=status.HTTP_200_OK)
async def get_book_published_date(published_date: int = Query(gt=1999, lt=2031)):
    book_list = []
    for book in BOOKS:
        if published_date == book.published_date:
            book_list.append(book)
    return book_list


@app.put("/books/update/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_book(book_request: BookRequest, book_id: int = Path(gt=0)):
    is_updated = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS[i] = Book(**book_request.model_dump())
            is_updated = True
    if not is_updated:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


@app.delete("/books/delete/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: int = Path(gt=0)):
    is_deleted = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            is_deleted = True
            break
    if not is_deleted:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")


def find_book_by_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
