from typing import Optional

from fastapi import Body, FastAPI
from pydantic import BaseModel, Field

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = Field(description="ID is not needed on create", default=None)
    title: str = Field(min_length=3, max_length=50)
    author: str = Field(min_length=3, max_length=50)
    description: str = Field(min_length=3, max_length=100)
    rating: int = Field(ge=0, le=5)

    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Mark cowell",
                "description": "A new description of the book",
                "rating": 3,
            }
        }
    }


BOOKS = [
    Book(1, "Computer Science Pro", "Jack Milter", "A very nice book!", 5),
    Book(2, "Python Essentials", "Laura Smith", "Comprehensive guide to Python.", 4),
    Book(3, "Advanced Django", "Megan Lee", "For Django enthusiasts.", 5),
    Book(4, "Data Science Handbook", "Alan Turing", "Deep dive into data science.", 5),
    Book(5, "Machine Learning Basics", "Tom Hawk", "Fundamentals of ML.", 4),
    Book(6, "Deep Learning Mastery", "Anna Bishop", "Insight into deep learning.", 5),
    Book(7, "Artificial Intelligence Primer", "John Doe", "Introduction to AI.", 4),
    Book(8, "React for Beginners", "Chris Pine", "Getting started with React.", 4),
    Book(9, "JavaScript Essentials", "Dana White", "JavaScript fundamentals.", 3),
    Book(10, "Cloud Computing Guide", "Sarah Connor", "Overview of cloud computing.", 4)
]


@app.get("/books")
async def get_books():
    return BOOKS


@app.post("/books")
async def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_by_id(new_book))


def find_book_by_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book