from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import backref

db = SQLAlchemy()

class Author(db.Model):
    __tablename__= 'authors'
    author_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), nullable=False)
    birth_date =db.Column(db.DateTime)
    date_of_death = db.Column(db.DateTime)

    books = db.relationship('Book', backref='author', lazy=True)

    def __repr__(self):
        return (f"Author(id={self.author_id}, name={self.name}, "
                f"birth_date={self.birth_date}, date_of_death={self.date_of_death})")


class Book(db.Model):
    __tablename__= 'books'
    book_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    isbn = db.Column(db.String)
    title =db.Column(db.String)
    publication_year = db.Column(db.Integer)

    author_id =db.Column(db.Integer, db.ForeignKey('authors.author_id'), nullable=False)


    def __repr__(self):
        return (f"Book(id={self.book_id}, isbn={self.isbn}, "
                f"title={self.title}, publication_year={self.publication_year}, author_id={self.author_id})")



