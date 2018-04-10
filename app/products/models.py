
from flask import url_for
from flask_login import current_user
from app import db
#from app.users.models import User
from app.billing.models import Rent
from app.utils.common import JsonResponse


books_authors_association = db.Table('books_authors',
                                     db.Model.metadata,
                                     db.Column('book_id',
                                               db.Integer,
                                               db.ForeignKey('books.id')),
                                     db.Column('author_id',
                                               db.Integer,
                                               db.ForeignKey('authors.id')))


books_genres_association = db.Table('books_genres',
                                     db.Model.metadata,
                                     db.Column('book_id',
                                               db.Integer,
                                               db.ForeignKey('books.id')),
                                     db.Column('genre_id',
                                               db.Integer,
                                               db.ForeignKey('genres.id')))


class Author(db.Model, JsonResponse):
    __tablename__ = 'authors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=30))
    email = db.Column(db.String(length=80))

    READONLY_FIELDS = ['id']
    REQUIRED_FIELDS = ['name']
    EDITABLE_FIELDS = ['name', 'email']

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }


class Publication(db.Model, JsonResponse):
    __tablename__ = 'publications'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=30))
    email = db.Column(db.String(length=80))

    READONLY_FIELDS = ['id']
    REQUIRED_FIELDS = ['name']
    EDITABLE_FIELDS = ['name', 'email']

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email
        }


class Genre(db.Model, JsonResponse):
    __tablename__ = 'genres'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=30))
    base_price = db.Column(db.Float, default=0)

    READONLY_FIELDS = ['id']
    REQUIRED_FIELDS = ['name']
    EDITABLE_FIELDS = ['name', 'base_price']

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'base_price': self.base_price
        }


class Currency(db.Model, JsonResponse):
    __tablename__ = 'currencies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=30))
    prefix = db.Column(db.String(length=4))
    base_value = db.Column(db.Float, default=0.0)

    READONLY_FIELDS = ['id']
    REQUIRED_FIELDS = ['name']
    EDITABLE_FIELDS = ['name', 'prefix', 'base_value']

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'prefix': self.prefix,
            'base_val': self.base_value
        }


class Book(db.Model, JsonResponse):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, default="")
    published_year = db.Column(db.String(length=4), default="1900")
    authors = db.relationship('Author', secondary=books_authors_association)
    publication_id = db.Column(db.Integer, db.ForeignKey('publications.id'))
    genres = db.relationship('Genre', secondary=books_genres_association)
    stock = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, default=0)
    currency_id = db.Column(db.Integer, db.ForeignKey('currencies.id'))
    added_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    READONLY_FIELDS = ['added_by', 'id']
    REQUIRED_FIELDS = ['name']
    EDITABLE_FIELDS = ['name', 'description', 'published_year', 'authors',
                       'publication_id', 'genres', 'stock', 'price',
                       'currency_id']

    @staticmethod
    def slugify(value):
        value = value.lower()
        len_string = len(value)
        for index in range(len_string):
            if not ('z' >= value[index] >= 'a'):
                value = value[:index] + "-" + value[index+1:]
        return value

    @property
    def slug(self):
        return self.slugify(self.name)

    @property
    def picture(self):
        return url_for('static', filename='books/%s.jpg' % self.slug)

    def is_already_issued(self):
        if current_user.is_anonymous:
            return False
        rents = Rent.query.all()
        for rent in rents:
            if rent.book_id == self.id and rent.user_id == current_user.id\
                    and not rent.status:
                return True
        return False

    def to_json(self):
        return {
            'url': url_for('products.get_book', id=self.id, _external=True),
            'name': self.name,
            'description': self.description,
            'slug': self.slug,
            'year': self.published_year,
            'authors': [author.to_json() for author in self.authors],
            'publication': Publication.query.get(self.publication_id).\
                to_json() if self.publication_id else {},
            'genres': [genre.to_json() for genre in self.genres],
            'stock': self.stock,
            'price': self.price,
            'picture': self.picture,
            'currency': Currency.query.get(self.currency_id).\
                to_json() if self.currency_id else {}
        }

    def from_json(self, json_data):
        if 'authors' in json_data:
            for author in json_data['authors']:
                author_obj = Author.query.get(author)
                self.authors.append(author_obj)
            del json_data['authors']

        if 'genres' in json_data:
            for genre in json_data['genres']:
                genre_obj = Genre.query.get(genre)
                self.genres.append(genre_obj)
            del json_data['genres']

        if 'publication_id' in json_data:
            self.publication_id = Publication.query.get(
                json_data['publication_id']).id

            del json_data['publication_id']

        if 'currency_id' in json_data:
            self.currency_id = Currency.query.get(json_data['currency_id']).id
            del json_data['currency_id']

        for key in json_data:
            if key in self.READONLY_FIELDS:
                raise ValueError("Field '%s' is read only" % key)
            elif key in self.REQUIRED_FIELDS and\
                            json_data.get(key) is None and\
                    not getattr(self, key):
                raise ValueError("Field '%s' is required")
            setattr(self, key, json_data.get(key))

        # TODO: Handle appropriately for logged in admin user only
        #self.added_by = User.query.all()[0].id

        return self
