from enum import unique

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref

db = SQLAlchemy()
#db becomes an instance of this classs

class Author(db.Model):
    """
        Represents an author in the database.

        Attributes:
            author_id (int): The unique identifier for the author.
            name (str): The name of the author.
            birth_date (datetime): The birthdate of the author.
            date_of_death (datetime): The death date of the author (if applicable).
            books (list): A list of books associated with the author.

        Methods:
            __repr__(): Returns a string representation of the Author object.
    """
    __tablename__ = 'authors'

    author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    birth_date = db.Column(db.DateTime)
    date_of_death = db.Column(db.DateTime)

    books = db.relationship('Book', back_populates='author', lazy=True)

    def __repr__(self):

        return (
                f"Author(id={self.author_id}, name={self.name}, "
                f"birth_date={self.birth_date}, date_of_death={self.date_of_death})"
            )


class Book(db.Model):
    """
        Represents a book in the database.

        Attributes:
            book_id (int): The unique identifier for the book.
            isbn (str): The ISBN number of the book.
            title (str): The title of the book.
            publication_year (int): The year the book was published.
            author_id (int): The unique identifier for the author of the book.

        Methods:
            __repr__(): Returns a string representation of the Book object.
        """
    __tablename__ = 'books'

    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String, nullable = False, unique = True)
    title = db.Column(db.String, nullable=False)
    publication_year = db.Column(db.Integer)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'), nullable=False)

    author = db.relationship('Author', back_populates='books')

    def __repr__(self):
        """
               Returns a string representation of the Book object.
        """
        return (
            f"Book(id={self.book_id}, isbn={self.isbn}, "
            f"title={self.title}, publication_year={self.publication_year}, "
            f"author_id={self.author_id})"
        )
