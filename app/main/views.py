
from flask import render_template
from . import main

from app import google_manager


@main.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html',
                           google_auth_url=google_manager.login_url())
