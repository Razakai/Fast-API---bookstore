from pydantic import BaseModel
from models.Author import Author


class Book(BaseModel):
    isbn: str
    name: str
    author: Author
    year: int
