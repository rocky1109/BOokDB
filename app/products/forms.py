
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, SelectField, \
    SubmitField, SelectMultipleField, IntegerField, FileField, DateTimeField, DateField
from wtforms.validators import Required, Length, Email, DataRequired
from datetime import datetime


class NewAuthorForm(FlaskForm):
    name = StringField("Author's Full name", validators=[Required()])
    email = StringField("Author's Email", validators=[Email()])
    save = SubmitField("Save")


class ManageAuthorForm(FlaskForm):
    name = StringField("Author's Full name", validators=[Required()])
    email = StringField("Author's Email", validators=[Email()])
    edit = SubmitField("Edit")
    delete = SubmitField("Delete")
    cancel = SubmitField("Cancel")


class NewPublicationForm(FlaskForm):
    name = StringField("Publication's Full name", validators=[Required()])
    email = StringField("Publication's Email", validators=[Email()])
    save = SubmitField("Save")


class ManagePublicationForm(FlaskForm):
    name = StringField("Publication's Full name", validators=[Required()])
    email = StringField("Publication's Email", validators=[Email()])
    edit = SubmitField("Edit")
    delete = SubmitField("Delete")
    cancel = SubmitField("Cancel")


class NewGenreForm(FlaskForm):
    name = StringField("Genre Name", validators=[Required()])
    base_price = FloatField("Base Rent for books from this Genre",
                            default=0)
    save = SubmitField("New")


class ManageGenreForm(FlaskForm):
    name = StringField("Genre Name", validators=[Required()])
    base_price = FloatField("Base Rent for books from this Genre",
                            default=0)
    edit = SubmitField("Edit")
    delete = SubmitField("Delete")
    cancel = SubmitField("Cancel")


class NewBookForm(FlaskForm):
    name = StringField("Book Name", validators=[Required()])
    description = TextAreaField("Description")
    published_year = StringField("Published in year")
    authors = SelectMultipleField("Author(s)", choices=[])
    publication_id = SelectField("Publication", choices=[])
    genres = SelectMultipleField("Genre(s)", choices=[])
    stock = IntegerField(default=0)
    price = FloatField("Rent for books (overrides the default price from genre)",
                            default=0)
    currency_id = SelectField("Currency", choices=[])
    picture = FileField("Select thumbnail for this book")
    save = SubmitField("New")


class ManageBookForm(FlaskForm):
    name = StringField("Book Name", validators=[Required()])
    description = TextAreaField("Description")
    published_year = StringField("Published in year")
    authors = SelectMultipleField("Author(s)", choices=[])
    publication_id = SelectField("Publication", choices=[])
    genres = SelectMultipleField("Genre(s)", choices=[])
    stock = IntegerField(default=0)
    price = FloatField("Rent for books (overrides the default price from genre)",
                            default=0)
    currency_id = SelectField("Currency", choices=[])
    edit = SubmitField("Edit")
    delete = SubmitField("Delete")
    cancel = SubmitField("Cancel")


class RentBookForm(FlaskForm):
    issue_date = DateField("Date of Issue", default=datetime.now(),
                               render_kw={'readonly': True})
    return_date = DateField("Estd. Return date", validators=[DataRequired()])
    submit = SubmitField("Issue")
