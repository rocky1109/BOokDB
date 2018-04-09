
import os
import const

from flask import redirect, url_for, render_template, request, flash
from flask_login import current_user
from app import db
from . import view_blueprint
from .forms import NewAuthorForm, ManageAuthorForm, \
    NewPublicationForm, ManagePublicationForm, NewGenreForm, ManageGenreForm, \
    NewBookForm, ManageBookForm
from .models import Author, Publication, Genre, Book, Currency
from werkzeug.utils import secure_filename


@view_blueprint.route('/authors/', methods=['GET', 'POST'])
def authors():
    form = NewAuthorForm()
    if form.validate_on_submit():
        author = Author()
        author.name = form.name.data
        author.email = form.email.data
        db.session.add(author)
        db.session.commit()
        return redirect(url_for('.authors'))
    authors = Author.query.all()
    return render_template('authors.html', form=form, authors=authors,
                           target_author=None)


@view_blueprint.route('/authors/<int:id>', methods=['GET', 'POST'])
def author(id):
    target_author = Author.query.get_or_404(id)
    form = ManageAuthorForm()

    if form.validate_on_submit():
        if form.edit.data:
            target_author.name = form.name.data
            target_author.email = form.email.data
            db.session.add(target_author)
            db.session.commit()
        elif form.delete.data:
            db.session.delete(target_author)
            db.session.commit()
        #elif form.cancel.data:
        return redirect(url_for('.authors'))

    form.name.data = target_author.name
    form.email.data = target_author.email

    authors = Author.query.all()

    return render_template('authors.html', form=form,
                           authors=authors, target_author=target_author)


@view_blueprint.route('/publications/', methods=['GET', 'POST'])
def publications():
    form = NewPublicationForm()
    if form.validate_on_submit():
        publication = Publication()
        publication.name = form.name.data
        publication.email = form.email.data
        db.session.add(publication)
        db.session.commit()
        return redirect(url_for('.publications'))
    publications = Publication.query.all()
    return render_template('publications.html', form=form,
                           publications=publications,
                           target_publication=None)


@view_blueprint.route('/publications/<int:id>', methods=['GET', 'POST'])
def publication(id):
    target_publication = Publication.query.get_or_404(id)
    form = ManagePublicationForm()

    if form.validate_on_submit():
        if form.edit.data:
            target_publication.name = form.name.data
            target_publication.email = form.email.data
            db.session.add(target_publication)
            db.session.commit()
        elif form.delete.data:
            db.session.delete(target_publication)
            db.session.commit()
        #elif form.cancel.data:
        return redirect(url_for('.publications'))

    form.name.data = target_publication.name
    form.email.data = target_publication.email

    publications = Publication.query.all()
    return render_template('publications.html', form=form,
                           publications=publications,
                           target_publication=target_publication)


@view_blueprint.route('/genres/', methods=['GET', 'POST'])
def genres():
    form = NewGenreForm()
    if form.validate_on_submit():
        genre = Genre()
        genre.name = form.name.data
        genre.base_price = form.base_price.data
        db.session.add(genre)
        db.session.commit()
        return redirect(url_for('.genres'))
    genres = Genre.query.all()
    return render_template('genres.html', form=form, genres=genres,
                           target_genre=None)


@view_blueprint.route('/genres/<int:id>', methods=['GET', 'POST'])
def genre(id):
    target_genre = Genre.query.get_or_404(id)
    form = ManageGenreForm()

    if form.validate_on_submit():
        if form.edit.data:
            target_genre.name = form.name.data
            target_genre.base_price = form.base_price.data
            db.session.add(target_genre)
            db.session.commit()
        elif form.delete.data:
            db.session.delete(target_genre)
            db.session.commit()
        #elif form.cancel.data:
        return redirect(url_for('.genres'))

    form.name.data = target_genre.name
    form.base_price.data = target_genre.base_price

    genres = Genre.query.all()
    return render_template('genres.html', form=form,
                           genres=genres, target_genre=target_genre)


@view_blueprint.route('/books/', methods=['GET', 'POST'])
def books():
    form = NewBookForm()
    form.authors.choices = [(str(author.id), author.name) for author in Author.query.all()]
    form.publication_id.choices = [(str(pub.id), pub.name) for pub in Publication.query.all()]
    form.genres.choices = [(str(genre.id), genre.name) for genre in Genre.query.all()]
    form.currency_id.choices = [(str(cur.id), cur.prefix) for cur in Currency.query.all()]
    if form.validate_on_submit():
        book = Book()
        book.name = form.name.data
        book.description = form.description.data
        book.published_year = form.published_year.data

        for author in form.authors.data:
            book.authors.append(Author.query.get(int(author)))

        book.publication_id = int(form.publication_id.data)

        for genre in form.genres.data:
            book.genres.append(Genre.query.get(int(genre)))

        book.currency_id = int(form.currency_id.data)

        book.stock = form.stock.data
        book.price = form.price.data
        book.added_by = current_user.id

        if form.picture.data:
            book_thumbnail = form.picture.data
            filename = secure_filename(book_thumbnail.filename)
            book_thumbnail.save(os.path.join(const.BOOKS_IMG_DIR,
                                             "%s.jpg" % book.slug))

        db.session.add(book)
        db.session.commit()

        return redirect(url_for('.books'))
    books = Book.query.all()
    return render_template('books.html', form=form, books=books,
                           target_book=None)


@view_blueprint.route('/books/<int:id>', methods=['GET', 'POST'])
def book(id):
    target_book = Book.query.get_or_404(id)
    form = ManageBookForm()

    form.authors.choices = [(str(author.id), author.name) for author in
                            Author.query.all()]
    form.publication_id.choices = [(str(pub.id), pub.name) for pub in
                                   Publication.query.all()]
    form.genres.choices = [(str(genre.id), genre.name) for genre in
                           Genre.query.all()]
    form.currency_id.choices = [(str(cur.id), cur.prefix) for cur in
                                Currency.query.all()]

    if form.validate_on_submit():
        if form.edit.data:
            target_book.name = form.name.data
            target_book.description = form.description.data
            target_book.published_year = form.published_year.data

            for author in form.authors.data:
                target_book.authors.append(Author.query.get(int(author)))

            target_book.publication_id = int(form.publication_id.data)

            for genre in form.genres.data:
                target_book.genres.append(Genre.query.get(int(genre)))

            target_book.currency_id = int(form.currency_id.data)

            target_book.stock = form.stock.data
            target_book.price = form.price.data

            db.session.add(target_book)
            db.session.commit()
        elif form.delete.data:
            db.session.delete(target_book)
            db.session.commit()
        #elif form.cancel.data:
        return redirect(url_for('.books'))

    form.name.data = target_book.name
    form.description.data = target_book.description
    form.published_year.data = target_book.published_year
    form.authors.data = [str(author.id) for author in target_book.authors]
    form.publication_id.data = str(target_book.publication_id)
    form.genres.data = str([genre.id for genre in target_book.genres])
    form.currency_id.data = str(target_book.currency_id)
    form.stock.data = target_book.stock
    form.price.data = target_book.price

    books = Book.query.all()
    return render_template('books.html', form=form,
                           books=books, target_book=target_book)
