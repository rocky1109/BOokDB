
import os
import const

from datetime import datetime
from flask import redirect, url_for, render_template
from flask_login import current_user, login_required
from app.utils.decorators import admin_required
from app.billing.models import Discount, Rent
from app import db
from . import view_blueprint
from .forms import NewAuthorForm, ManageAuthorForm, \
    NewPublicationForm, ManagePublicationForm, NewGenreForm, ManageGenreForm, \
    NewBookForm, ManageBookForm, RentBookForm
from .models import Author, Publication, Genre, Book, Currency
from werkzeug.utils import secure_filename


@view_blueprint.route('/authors/', methods=['GET', 'POST'])
@admin_required
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
@admin_required
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
@admin_required
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
@admin_required
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
@admin_required
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
@admin_required
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
@admin_required
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
@admin_required
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

            target_book.authors = [Author.query.get(int(author))
                                   for author in form.authors.data]

            target_book.publication_id = int(form.publication_id.data)

            target_book.genres = [Genre.query.get(int(genre))
                                  for genre in form.genres.data]

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
    form.genres.data = [str(genre.id) for genre in target_book.genres]
    form.currency_id.data = str(target_book.currency_id)
    form.stock.data = target_book.stock
    form.price.data = target_book.price

    books = Book.query.all()
    return render_template('books.html', form=form,
                           books=books, target_book=target_book)


@view_blueprint.route('/books/<int:id>/rent', methods=['GET', 'POST'])
@login_required
def rent(id):
    form = RentBookForm()
    book = Book.query.get_or_404(id)

    if form.validate_on_submit():
        book.stock -= 1
        rent = Rent()
        rent.book_id = book.id
        rent.user_id = current_user.id
        rent.issue_timestamp = datetime.now()
        rent.return_timestamp = datetime.now()
        db.session.add(book)
        db.session.add(rent)
        db.session.commit()
        return redirect(url_for('main.index'))

    discounts = Discount.query.all()
    target_discounts = list()
    for discount in discounts:
        if book in discount.books:
            applicable_discounts = [item for item in discounts.books
                                    if item.id == book.id]

            target_discounts.extend(applicable_discounts)

    for discount in discounts:
        if any([item in discount.genres for item in book.genres]):
            # applicable_discounts = [item for item in discount
            #                         if any([v in item.genres
            #                                 for v in book.genres])]

            target_discounts.append(discount)

    discount_lowest_price = None
    for val in target_discounts:
        if discount_lowest_price is None or discount_lowest_price > val.calculate():
            discount_lowest_price = val.calculate()

    # applied_discounts = [val.name for val in target_discounts]

    return render_template("book_rent.html", book=book, form=form,
                           applied_discounts=target_discounts,
                           book_currency=Currency.query.get(book.currency_id),
                           discount_lowest_price=discount_lowest_price)


@view_blueprint.route('/books/<int:id>/return', methods=['GET', 'POST'])
@login_required
def return_book(id):
    book = Book.query.get_or_404(id)
    rent = Rent.query.filter_by(book_id=book.id, user_id=current_user.id,
                                status=False).first()
    if rent is None:
        return render_template("404.html")
    book.stock += 1
    rent.return_timestamp = datetime.now()
    rent.status = True
    rent.total = rent.calculate(
        elapsed_days=(datetime.now() - rent.issue_timestamp).days)
    db.session.add(book)
    db.session.add(rent)
    return redirect(url_for('main.index'))
