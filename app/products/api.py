
from flask import request, current_app, url_for, jsonify
from flask_login import current_user

from app import db

from . import api_blueprint
from .models import Book, Genre, Publication, Author, Currency


# ------ Views for *Book* model ------

@api_blueprint.route('/books/')
def get_books():
    page = request.args.get('page', 1, type=int)
    pagination = Book.query.paginate(
        page, per_page=current_app.config['RESULTS_PER_PAGE']
    )
    books = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('products.get_books', page=page - 1, _external=True)

    next = None
    if pagination.has_next:
        prev = url_for('products.get_books', page=page + 1, _external=True)

    return jsonify({
        'results': [book.to_json() for book in books],
        'prev': prev,
        'next': next,
        'count': pagination.total
    })


@api_blueprint.route('/books/<int:id>')
def get_book(id):
    book = Book.query.get_or_404(id)
    return jsonify(book.to_json())


@api_blueprint.route('/books/', methods=['POST'])
def new_book():
    book = Book().from_json(request.json)
    # book.added_by = current_user
    # import pdb; pdb.set_trace()
    #
    # authors = book.authors
    # book.authors = Book.authors
    # for author in [Author.query.get(author_id) for author_id in authors]:
    #     book.authors.append(author)
    #
    # genres = book.genres
    # book.genres = Book.authors
    # for genre in [Genre.query.get(genre_id) for genre_id in genres]:
    #     book.genres.append(genre)
    #
    # book.publication_id = Publication.query.get(book.publication_id)
    # book.currency_id = Currency.query.get(book.currency_id)

    try:
        db.session.add(book)
    except Exception as err:
        import pdb; pdb.set_trace()
        pass
    db.session.commit()
    return jsonify(book.to_json()), 201, \
           {'Location': url_for('products.get_book', id=book.id, _external=True)}


@api_blueprint.route('/books/<int:id>', methods=['PUT'])
def edit_book(id):
    book = Book.query.get_or_404(id)
    book.from_json(request.json)
    db.session.add(book)
    return jsonify(book.to_json())


# ------ Views for *Genre* model ------

@api_blueprint.route('/genres/')
def get_genres():
    genres = Genre.query.all()
    return jsonify({
        'results': [genre.to_json() for genre in genres],
        'count': len(genres)
    })


@api_blueprint.route('/genres/<int:id>')
def get_genre(id):
    genre = Genre.query.get_or_404(id)
    return jsonify(genre.to_json())


@api_blueprint.route('/genres/', methods=['POST'])
def new_genre():
    genre = Genre().from_json(request.json)
    genre.added_by = current_user
    db.session.add(genre)
    db.session.commit()
    return jsonify(genre.to_json()), 201, \
           {'Location': url_for('products.get_genre', id=genre.id,
                                _external=True)}


@api_blueprint.route('/genres/<int:id>', methods=['PUT'])
def edit_genre(id):
    genre = Genre.query.get_or_404(id)
    genre.from_json(request.json)
    db.session.add(genre)
    return jsonify(genre.to_json())


# ------ Views for *Author* model ------

@api_blueprint.route('/authors/')
def get_authors():
    authors = Author.query.all()
    return jsonify({
        'results': [author.to_json() for author in authors],
        'count': len(authors)
    })


@api_blueprint.route('/authors/<int:id>')
def get_author(id):
    author = Author.query.get_or_404(id)
    return jsonify(author.to_json())


@api_blueprint.route('/authors/', methods=['POST'])
def new_author():
    author = Author().from_json(request.json)
    author.added_by = current_user
    db.session.add(author)
    db.session.commit()
    return jsonify(author.to_json()), 201, \
           {'Location': url_for('products.get_author', id=author.id,
                                _external=True)}


@api_blueprint.route('/authors/<int:id>', methods=['PUT'])
def edit_author(id):
    author = Author.query.get_or_404(id)
    author.from_json(request.json)
    db.session.add(author)
    return jsonify(author.to_json())


# ------ Views for *Publication* model ------

@api_blueprint.route('/publications/')
def get_publications():
    publications = Publication.query.all()
    return jsonify({
        'results': [publication.to_json() for publication in publications],
        'count': len(publications)
    })


@api_blueprint.route('/publications/<int:id>')
def get_publication(id):
    publication = Publication.query.get_or_404(id)
    return jsonify(publication.to_json())


@api_blueprint.route('/publications/', methods=['POST'])
def new_publication():
    publication = Publication().from_json(request.json)
    publication.added_by = current_user
    db.session.add(publication)
    db.session.commit()
    return jsonify(publication.to_json()), 201, \
           {'Location': url_for('products.get_publication', id=publication.id,
                                _external=True)}


@api_blueprint.route('/publications/<int:id>', methods=['PUT'])
def edit_publication(id):
    publication = Publication.query.get_or_404(id)
    publication.from_json(request.json)
    db.session.add(publication)
    return jsonify(publication.to_json())


# ------ Views for *Currency* model ------

@api_blueprint.route('/currencies/')
def get_currencies():
    currencies = Currency.query.all()
    return jsonify({
        'results': [currency.to_json() for currency in currencies],
        'count': len(currencies)
    })


@api_blueprint.route('/currencies/<int:id>')
def get_currency(id):
    currency = Currency.query.get_or_404(id)
    return jsonify(currency.to_json())


@api_blueprint.route('/currencies/', methods=['POST'])
def new_currency():
    currency = Currency().from_json(request.json)
    currency.added_by = current_user
    db.session.add(currency)
    db.session.commit()
    return jsonify(currency.to_json()), 201, \
           {'Location': url_for('products.get_currency', id=currency.id,
                                _external=True)}


@api_blueprint.route('/currencies/<int:id>', methods=['PUT'])
def edit_currency(id):
    currency = Currency.query.get_or_404(id)
    currency.from_json(request.json)
    db.session.add(currency)
    return jsonify(currency.to_json())
