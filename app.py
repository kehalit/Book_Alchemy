
import os
from flask import Flask,render_template,request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
database_path = os.path.join(basedir, 'data', 'library.sqlite')

app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


db.init_app(app)

with app.app_context():
  db.create_all()

@app.route('/')
def home():
    return "Hello from the Book Library!"

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
            flash (f"An error occured:{str(e)}.', 'error' ")
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

            #create a new Book instance
            book = Book(isbn=isbn, title=title, publication_year=publication_year, author_id=author_id)


            # Add the new book to the database
            db.session.add(book)
            db.session.commit()

            flash('Book successfully added!', 'success')
            return redirect(url_for('add_book'))

        except Exception as e:
            #db.session.rollback()
            flash (f"An error occured:{str(e)}.', 'error' ")
            return redirect(url_for('add_book'))

    # GET request - fetch authors for the dropdown
    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)

if __name__ == '__main__':
    app.run(debug=True)