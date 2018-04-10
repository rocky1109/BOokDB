
from datetime import datetime
from flask import redirect, url_for, render_template
from flask_login import current_user, login_required
from app import db
from app.utils.decorators import admin_required
from app.products.models import Book, Genre, Currency
from . import view_blueprint
from .forms import NewDiscountForm, NewRuleForm, NewConditionForm, \
    ManageConditionForm, ManageDiscountForm, ManageRuleForm
from .models import Discount, Condition, Rule, RULE_MAP, CONDITION_MAP, Rent


@view_blueprint.route('/discounts/', methods=['GET', 'POST'])
@admin_required
def discounts():
    form = NewDiscountForm()
    form.books.choices = [(str(book.id), book.name) for book in Book.query.all()]
    form.genres.choices = [(str(genre.id), genre.name) for genre in Genre.query.all()]
    form.rules.choices = [(str(rule.id), rule.name) for rule in Rule.query.all()]
    if form.validate_on_submit():
        discount = Discount()
        discount.name = form.name.data

        for book in form.books.data:
            discount.books.append(Book.query.get(int(book)))

        for genre in form.genres.data:
            discount.genres.append(Genre.query.get(int(genre)))

        for rule in form.rules.data:
            discount.rules.append(Rule.query.get(int(rule)))

        db.session.add(discount)
        db.session.commit()
        return redirect(url_for('.discounts'))
    discounts = Discount.query.all()
    return render_template('discounts.html', discounts=discounts,
                           target_discount=None, form=form)


@view_blueprint.route('/discounts/<int:id>', methods=['GET', 'POST'])
@admin_required
def discount(id):
    target_discount = Discount.query.get_or_404(id)
    form = ManageDiscountForm()
    form.books.choices = [(str(book.id), book.name) for book in Book.query.all()]
    form.genres.choices = [(str(genre.id), genre.name) for genre in Genre.query.all()]
    form.rules.choices = [(str(rule.id), rule.name) for rule in Rule.query.all()]
    if form.validate_on_submit():
        if form.edit.data:
            target_discount.name = form.name.data

            target_discount.books = [Book.query.get(int(book))
                                     for book in form.books.data]

            target_discount.genres = [Genre.query.get(int(genre))
                                      for genre in form.genres.data]

            target_discount.rules = [Rule.query.get(int(rule))
                                     for rule in form.rules.data]

            db.session.add(target_discount)
            db.session.commit()
        elif form.delete.data:
            db.session.delete(target_discount)
            db.session.commit()
        return redirect(url_for('.discounts'))

    form.name.data = target_discount.name

    form.books.data = [str(book.id) for book in target_discount.books]
    form.genres.data = [str(genre.id) for genre in target_discount.genres]
    form.rules.data = [str(rule.id) for rule in target_discount.rules]

    discounts = Discount.query.all()
    return render_template('discounts.html', discounts=discounts,
                           target_conditon=target_discount, form=form)


@view_blueprint.route('/rules/', methods=['GET', 'POST'])
@admin_required
def rules():
    form = NewRuleForm()
    form.rule_type.choices = [(i,i) for i in RULE_MAP.keys()]
    form.conditions.choices = [(str(c.id), c.name) for c in Condition.query.all()]
    if form.validate_on_submit():
        rule = Rule()
        rule.name = form.name.data
        rule.rule_type = form.rule_type.data

        rule.conditions = [Condition.query.get(int(cond))
                           for cond in form.conditions.data]

        db.session.add(rule)
        db.session.commit()
        return redirect(url_for('.rules'))
    rules = Rule.query.all()
    return render_template('rules.html', rules=rules, target_rule=None,
                           form=form)


@view_blueprint.route('/rules/<int:id>', methods=['GET', 'POST'])
@admin_required
def rule(id):
    target_rule = Rule.query.get_or_404(id)
    form = ManageRuleForm()
    form.rule_type.choices = [(i, i) for i in RULE_MAP.keys()]
    form.conditions.choices = [(str(c.id), c.name) for c in Condition.query.all()]
    if form.validate_on_submit():
        if form.edit.data:
            target_rule.name = form.name.data
            target_rule.rule_type = form.rule_type.data
            target_rule.days = form.days.data
            target_rule.price = form.price.data
            db.session.add(target_rule)
            db.session.commit()
        elif form.delete.data:
            db.session.delete(target_rule)
            db.session.commit()
        return redirect(url_for('.rules'))

    form.name.data = target_rule.name
    form.rule_type.data = target_rule.rule_type

    form.conditions.data = [str(cond.id) for cond in target_rule.conditions]

    rules = Rule.query.all()
    return render_template('rules.html', rules=rules,
                           target_conditon=target_rule, form=form)


@view_blueprint.route('/conditions/', methods=['GET', 'POST'])
@admin_required
def conditions():
    form = NewConditionForm()
    form.condition_type.choices = [(i,i) for i in CONDITION_MAP.keys()]
    if form.validate_on_submit():
        condition = Condition()
        condition.name = form.name.data
        condition.condition_type = form.condition_type.data
        condition.days = form.days.data
        condition.price = form.price.data
        db.session.add(condition)
        db.session.commit()
        return redirect(url_for('.conditions'))
    conditions = Condition.query.all()
    return render_template('conditions.html', conditions=conditions,
                           target_conditon=None, form=form)


@view_blueprint.route('/conditions/<int:id>', methods=['GET', 'POST'])
@admin_required
def condition(id):
    target_condition = Condition.query.get_or_404(id)
    form = ManageConditionForm()
    form.condition_type.choices = [(i, i) for i in CONDITION_MAP.keys()]
    if form.validate_on_submit():
        if form.edit.data:
            target_condition.name = form.name.data
            target_condition.condition_type = form.condition_type.data
            target_condition.days = form.days.data
            target_condition.price = form.price.data
            db.session.add(target_condition)
            db.session.commit()
        elif form.delete.data:
            db.session.delete(target_condition)
            db.session.commit()
        return redirect(url_for('.conditions'))

    form.name.data = target_condition.name
    form.condition_type.data = target_condition.condition_type
    form.price.data = target_condition.price
    form.days.data = target_condition.days

    conditions = Condition.query.all()
    return render_template('conditions.html', conditions=conditions,
                           target_conditon=target_condition, form=form)


@view_blueprint.route('/rentals/', methods=['GET', 'POST'])
@login_required
def rentals():
    rents = [rent for rent in Rent.query.all()
             if rent.user_id == current_user.id]
    books = [Book.query.get(rent.book_id) for rent in rents]
    currencies = [Currency.query.get(book.currency_id) for book in books]

    dirty = False
    outstanding_amounts = list()
    elapsed_days = list()
    for rent in rents:
        if rent.status:
            outstanding_amounts.append(rent.total)
            elapsed_days.append(None)
        else:
            days_passed = (datetime.now() - rent.issue_timestamp).days
            elapsed_days.append(days_passed)
            outstanding_amounts.append(rent.calculate(elapsed_days=days_passed))

        if not rent.read:
            dirty = True
            rent.read = True
            db.session.add(rent)

    if dirty:
        db.session.commit()

    return render_template('rentals.html', rentals=zip(rents, books, currencies, outstanding_amounts, elapsed_days))
