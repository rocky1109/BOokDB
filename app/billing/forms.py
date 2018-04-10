
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, SelectField, \
    SubmitField, SelectMultipleField, IntegerField, FileField
from wtforms.validators import Required, Length, Email, DataRequired
from wtforms import ValidationError


class NewDiscountForm(FlaskForm):
    name = StringField("Discount Name", validators=[DataRequired()])
    books = SelectMultipleField("Book(s)", choices=[])
    genres = SelectMultipleField("Genre(s)", choices=[])
    rules = SelectMultipleField("Rule(s)", choices=[])
    save = SubmitField("Apply")


class ManageDiscountForm(FlaskForm):
    name = StringField("Discount Name", validators=[DataRequired()])
    books = SelectMultipleField("Book(s)", choices=[])
    genres = SelectMultipleField("Genre(s)", choices=[])
    rules = SelectMultipleField("Rule(s)", choices=[])
    edit = SubmitField("Edit")
    delete = SubmitField("Delete")
    cancel = SubmitField("Cancel")


class NewRuleForm(FlaskForm):
    name = StringField("Rule Name", validators=[DataRequired()])
    rule_type = SelectField("Rule Type", choices=[])
    conditions = SelectMultipleField("Condition(s)", choices=[])
    save = SubmitField("Save")


class ManageRuleForm(FlaskForm):
    name = StringField("Rule Name", validators=[DataRequired()])
    rule_type = SelectField("Rule Type", choices=[])
    conditions = SelectMultipleField("Condition(s)", choices=[])
    edit = SubmitField("Edit")
    delete = SubmitField("Delete")
    cancel = SubmitField("Cancel")


class NewConditionForm(FlaskForm):
    name = StringField("Condition Name", validators=[DataRequired()])
    days = IntegerField("Days", validators=[DataRequired()])
    condition_type = SelectField("Rule Type", choices=[])
    price = FloatField("Price", validators=[DataRequired()])
    save = SubmitField("Save")


class ManageConditionForm(FlaskForm):
    name = StringField("Condition Name", validators=[DataRequired()])
    days = IntegerField("Days", validators=[DataRequired()])
    condition_type = SelectField("Rule Type", choices=[])
    price = FloatField("Price", validators=[DataRequired()])
    edit = SubmitField("Edit")
    delete = SubmitField("Delete")
    cancel = SubmitField("Cancel")
