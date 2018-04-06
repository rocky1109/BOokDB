
from flask import render_template
from . import main

from app import google_manager
from app.products.models import Book


@main.route('/', methods=['GET', 'POST'])
def index():
    books = Book.query.all()
    return render_template('index.html',
                           google_auth_url=google_manager.login_url(),
                           books=books)
