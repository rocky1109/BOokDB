
import json

from flask import redirect, url_for, session, flash
from flask_login import login_user, logout_user

from app.users.models import User
from app import google_manager, db
from . import auth


def create_or_get_user(user_details, token):
    """
    {'sub': '108756046399083923726', 'name': 'roc e',
    'given_name': 'roc', 'family_name': 'e',
    'profile': 'https://plus.google.com/108756046399083923726',
    'picture': 'https://lh3.googleusercontent.com/-XdUIqdMkCWA/AAAAAAAAAAI/AAAAAAA
AAAA/4252rscbv5M/photo.jpg',
    'email': 'royrocky1109@gmail.com',
    'email_verified': True,
    'gender': 'male'}

    :param user_details:
    :return:
    """
    user = User.query.filter_by(email=user_details['email']).first()
    if user is None:
        user = User()
        user.email = user_details['email']
        user.first_name = user_details['given_name']
        user.last_name = user_details['family_name']
        user.picture = user_details['picture']
        user.access_token = token['access_token']
        db.session.add(user)
        db.session.commit()
    return user


@auth.route('/callback/google')
@google_manager.oauth2callback
def login(token, userinfo, **params):
    user = create_or_get_user(user_details=userinfo, token=token)
    login_user(user)
    session['token'] = json.dumps(token)
    session['extra'] = params.get('extra')
    return redirect(params.get('next', url_for('main.index')))


@auth.route('/logout')
def logout():
    logout_user()
    session.clear()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))


@google_manager.user_loader
def load_user(user_email):
    return User.query.filter_by(email=user_email).first()
