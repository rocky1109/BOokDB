
from enum import Enum
from datetime import datetime

from app import db
from app.utils.conditions import ConditionHelper, RuleHelper


discount_books_association = db.Table('discount_books',
                                     db.Model.metadata,
                                     db.Column('discount_id',
                                               db.Integer,
                                               db.ForeignKey('discounts.id')),
                                     db.Column('book_id',
                                               db.Integer,
                                               db.ForeignKey('books.id')))

discount_genres_association = db.Table('discount_genres',
                                     db.Model.metadata,
                                     db.Column('discount_id',
                                               db.Integer,
                                               db.ForeignKey('discounts.id')),
                                     db.Column('genre_id',
                                               db.Integer,
                                               db.ForeignKey('genres.id')))

discount_rules_association = db.Table('discount_rules',
                                     db.Model.metadata,
                                     db.Column('discount_id',
                                               db.Integer,
                                               db.ForeignKey('discounts.id')),
                                     db.Column('rule_id',
                                               db.Integer,
                                               db.ForeignKey('rules.id')))

rule_condition_association = db.Table('rule_conditions',
                                     db.Model.metadata,
                                     db.Column('rule_id',
                                               db.Integer,
                                               db.ForeignKey('rules.id')),
                                     db.Column('condition_id',
                                               db.Integer,
                                               db.ForeignKey('conditions.id')))


CONDITION_MAP = {f.__name__: f for f in [ConditionHelper.less_than,
                                         ConditionHelper.less_than_or_equal,
                                         ConditionHelper.greater_than,
                                         ConditionHelper.greater_than_or_equal]}


RULE_MAP = {f.__name__: f for f in [RuleHelper.tariff_range,
                                    RuleHelper.min_charges]}


class ConditionType(Enum):
    less_than = 'less_than'
    greater_than = 'greater_than'
    less_than_or_equal = 'less_than_or_equal'
    greater_than_or_equal = 'greater_than_or_equal'


class RuleType(Enum):
    tariff_range = 'tariff_range'
    min_charges = 'min_charges'


class Rent(db.Model):
    __tablename__ = 'rents'

    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    issue_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    return_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    total = db.Column(db.Float, default=0)
    status = db.Column(db.Boolean, default=False)
    read = db.Column(db.Boolean, default=False)

    def calculate(self, elapsed_days):
        from app.products.models import Book, Genre

        discounts = Discount.query.all()
        target_discounts = list()
        for discount in discounts:
            for book in discount.books:
                if book.id == self.book_id:
                    target_discounts.append(discount)
            for genre in discount.genres:
                if any([genre in Book.query.get(self.book_id).genres]):
                    target_discounts.append(discount)
        calculated_discounts = [discount.calculate(elapsed_days=elapsed_days)
                               for discount in target_discounts]
        if calculated_discounts:
            return min(calculated_discounts)
        else:
            book = Book.query.get(self.book_id)
            return min([genre.base_price for genre in book.genres])


class Condition(db.Model):
    __tablename__ = 'conditions'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=80))
    days = db.Column(db.Integer, default=0)
    price = db.Column(db.Float, default=0)
    condition_type = db.Column(db.Enum(ConditionType))

    @property
    def available_conditions(self):
        return CONDITION_MAP.keys()

    def calculate(self, elapsed_days):
        condition_func = getattr(ConditionHelper, self.condition_type.value)
        return condition_func(days=self.days, price=self.price,
                              elapsed_days=elapsed_days)


class Rule(db.Model):
    __tablename__ = 'rules'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(length=80))
    rule_type = db.Column(db.Enum(RuleType))
    conditions = db.relationship('Condition',
                                 secondary=rule_condition_association)

    @property
    def available_rules(self):
        return RULE_MAP.keys()

    def calculate(self, elapsed_days):
        rule_func = getattr(RuleHelper, self.rule_type.value)
        condition_values = {condition.name: condition.calculate(elapsed_days)
                            for condition in self.conditions}
        return rule_func(conditions=condition_values)


class Discount(db.Model):
    __tablename__ = 'discounts'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    books = db.relationship('Book', secondary=discount_books_association)
    genres = db.relationship('Genre', secondary=discount_genres_association)
    rules = db.relationship('Rule', secondary=discount_rules_association)

    def calculate(self, elapsed_days=1):
        _ = {rule.name: rule.calculate(elapsed_days) for rule in self.rules}
        return max(_.values())
