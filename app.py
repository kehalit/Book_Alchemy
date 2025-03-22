import os
from crypt import methods
import requests
from flask import Flask,render_template,request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

API_URL = os.getenv('API_URL')
basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'data', 'library.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

db.init_app(app)


def fetch_cover_picture(isbn):
    try:
        url = f'{API_URL}{isbn}-L.jpg'  # Assuming the API_URL gives direct access to images.
        response = requests.get(url)
        if response.status_code == 200:
            return url  # Return the image URL directly if the request is successful
        else:
            return 'default_image.jpg'  # Return a default image if not found
    except Exception as e:
        print(f"Error fetching cover image: {e}")
        return 'default_image.jpg'

with app.app_context():
  db.create_all()


@app.route('/', methods= ['GET'])
def home():
    search_term = request.args.get('search', '')
    sort_by = request.args.get('sort_by', 'title')
    query = Book.query.join(Author)

    if search_term:
        query = query.filter(
                Book.title.ilike(f'%{search_term}%') | Author.name.ilike(f'%{search_term}%')
             )
    if sort_by == 'author':
        query = query.order_by(Author.name)
    else:
        query =query.order_by(Book.title)

    books = query.all()
    for book in books:
        cover_image = fetch_cover_picture(book.isbn)
        book.cover_image = cover_image

    return render_template('home.html', books=books, sort_by=sort_by, search_term=search_term)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':

        name = request.form['name']
        birth_date_str = request.form['birth_date']
        date_of_death_str = request.form['date_of_death']

        # Add the new author to the database
        try:
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
            date_of_death = None
            if date_of_death_str:
                date_of_death = datetime.strptime(date_of_death_str, '%Y-%m-%d').date()
            # Create a new Author object
            author = Author(name=name, birth_date=birth_date, date_of_death=date_of_death)
            db.session.add(author)
            db.session.commit()
            flash('Author successfully added!', 'success')
            return redirect(url_for('add_author'))
        except Exception as e:
            db.session.rollback()
            flash (f"An error occured:{str(e)}", 'error' )
            return redirect(url_for('add_author'))
    # If GET request, just render the form
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        try:
            title = request.form['title']
            isbn = request.form['isbn']
            publication_year = request.form['publication_year']
            author_id = request.form['author_id']

            if not author_id:
                flash('Author is required for a book.', 'error')
                return redirect(url_for('add_book'))
            author_id =int(author_id)

            #create a new Book instance
            book = Book(isbn=isbn, title=title, publication_year=publication_year, author_id=author_id)

            # Add the new book to the database
            db.session.add(book)
            db.session.commit()

            flash('Book successfully added!', 'success')
            return redirect(url_for('add_book'))

        except Exception as e:
            #db.session.rollback()
            flash (f"An error occured:{str(e)} ", 'error' )
            return redirect(url_for('add_book'))

    # GET request - fetch authors for the dropdown
    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


@app.route('/book/<int:book_id>/delete', methods=['POST'])
def delete_book(book_id):
    # Find the book to delete
    book = Book.query.get_or_404(book_id)

    # Save the author of the book
    author = book.author

    # Delete the book from the database
    db.session.delete(book)

    # Check if the author has any other books
    if not Author.query.filter_by(author_id=author.author_id).first():
        # If the author has no other books, delete the author as well
        db.session.delete(author)

    db.session.commit()
    # Flash a success message
    flash(f'Book "{book.title}" has been successfully deleted!', 'success')
    # Redirect to the homepage
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)