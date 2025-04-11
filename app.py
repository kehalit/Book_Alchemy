import os
import requests
from flask import (
    Flask, render_template, request,
    redirect, url_for, flash
)
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Flask application setup
app = Flask(__name__)

# Environment variables
API_URL = os.getenv('API_URL')

# Database configuration
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'data', 'library.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

# Initialize the database with Flask app
db.init_app(app)


def fetch_cover_picture(isbn):
    """
    Fetches the cover picture URL for a book using its ISBN.

    Args:
        isbn (str): The ISBN number of the book.

    Returns:
        str: URL of the cover image or a default image.
    """
    try:
        timeout_duration = 10
        url = f'{API_URL}{isbn}-L.jpg'
        response = requests.get(url, timeout = timeout_duration)
        if response.status_code == 200:
            return url
        return 'default_image.jpg'

    except Exception as e:
        print(f"Error fetching cover image: {e}")
        return 'default_image.jpg'


# Create database tables within app context
with app.app_context():
    db.create_all()


@app.route('/', methods=['GET'])
def home():
    """
    Displays the homepage with a list of books,
    allowing search and sorting options.
    """
    search_term = request.args.get('search', '')
    sort_by = request.args.get('sort_by', 'title')

    query = Book.query.join(Author)

    if search_term:
        query = query.filter(
            Book.title.ilike(f'%{search_term}%') |
            Author.name.ilike(f'%{search_term}%')
        )

    if sort_by == 'author':
        query = query.order_by(Author.name)
    else:
        query = query.order_by(Book.title)

    books = query.all()

    # Attach cover images to book objects
    for book in books:
        cover_image = fetch_cover_picture(book.isbn)
        book.cover_image = cover_image

    return render_template(
        'home.html',
        books=books,
        sort_by=sort_by,
        search_term=search_term
    )


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
    Adds a new author to the database.

    GET: Renders the author form.
    POST: Handles submission of a new author.
    """
    if request.method == 'POST':
        name = request.form['name']
        birth_date_str = request.form['birth_date']
        date_of_death_str = request.form['date_of_death']

        try:
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            date_of_death = None
            if date_of_death_str:
                date_of_death = datetime.strptime(
                    date_of_death_str, '%Y-%m-%d'
                ).date()

            author = Author(
                name=name,
                birth_date=birth_date,
                date_of_death=date_of_death
            )

            db.session.add(author)
            db.session.commit()

            flash('Author successfully added!', 'success')
            return redirect(url_for('add_author'))

        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", 'error')
            return redirect(url_for('add_author'))

    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    """
    Adds a new book to the database.

    GET: Renders the book form.
    POST: Handles submission of a new book.
    """
    if request.method == 'POST':
        try:
            title = request.form['title']
            isbn = request.form['isbn']
            publication_year = request.form['publication_year']
            author_id = request.form['author_id']

            if not author_id:
                flash('Author is required for a book.', 'error')
                return redirect(url_for('add_book'))

            author_id = int(author_id)

            book = Book(
                isbn=isbn,
                title=title,
                publication_year=publication_year,
                author_id=author_id
            )

            db.session.add(book)
            db.session.commit()

            flash('Book successfully added!', 'success')
            return redirect(url_for('add_book'))

        except Exception as e:
            db.session.rollback()
            flash(f"An error occurred: {str(e)}", 'error')
            return redirect(url_for('add_book'))

    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    """
    Deletes a book from the database and, if the author has no
    remaining books, deletes the author as well.

    Args:
        book_id (int): The ID of the book to delete.
    """
    book = Book.query.get_or_404(book_id)
    author = book.author

    db.session.delete(book)

    remaining_books = Book.query.filter_by(author_id=author.author_id).count()

    if remaining_books == 0:
        db.session.delete(author)

    db.session.commit()

    flash(f'Book "{book.title}" has been successfully deleted!', 'success')
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)
