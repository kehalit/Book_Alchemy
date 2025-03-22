## Flask Library Management System
A simple library management system built with Flask, SQLAlchemy, and SQLite. This project allows users to manage authors and books, including adding, deleting, and viewing them. It also fetches book cover images via an external API.

## Features
Author Management: Add and manage authors with birth and death dates.

Book Management: Add books with titles, ISBN, publication year, and associate them with authors.

Search & Sort: Search books and authors, and sort books by title or author name.

Cover Images: Fetch book cover images using an external API based on ISBN.

## Requirements
Python 3.x

Flask

Flask-SQLAlchemy

requests

python-dotenv

##Installation
Clone this repository:

git clone https://github.com/kehalit/Book_Alchemy.git
cd library-management-system
Create a virtual environment:

python3 -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
Install the required dependencies:

pip install -r requirements.txt
Create a .env file and add your environment variables (such as API_URL and SECRET_KEY):

API_URL="your-api-url"
SECRET_KEY="your-secret-key"
Initialize the database:

flask db init
flask db migrate
flask db upgrade
Usage
Run the Flask app:

python app.py
Open your browser and go to http://127.0.0.1:5000/ to access the app.

## Routes
/: Home page displaying a list of books with search and sort functionality.

/add_author: Page to add a new author.

/add_book: Page to add a new book.

/book/<int:book_id>/delete: Route to delete a specific book from the database.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

