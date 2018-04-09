
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, AnonymousUserMixin
from flask_bootstrap import Bootstrap

from config import configurations
from app.utils.google_oauth import GoogleOAuthManager


db = SQLAlchemy()


class AnonymousUser(AnonymousUserMixin):
    name = "Guest"
    is_admin = False


login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.anonymous_user = AnonymousUser

google_manager = GoogleOAuthManager(login_manager=login_manager)

bootstrap = Bootstrap()


def initialize_apps(apps, flask_app):
    for app in apps:
        app.init_app(app=flask_app)


def register_blueprints(app, blueprints):
    for blueprint in blueprints:
        app.register_blueprint(blueprint, url_prefix=blueprints[blueprint])


def create_app(config_name=None):
    app = Flask(__name__,
                static_folder=configurations[config_name].STATIC_DIR,
                template_folder=configurations[config_name].TEMPLATE_DIR)
    config_env = os.environ.get('IS_HEROKU')
    if config_env == True or config_env == 'True':
        config_name = 'heroku'
    app.config.from_object(configurations[config_name])

    initialize_apps(flask_app=app, apps=[db,
                                         login_manager,
                                         google_manager,
                                         bootstrap])

    from .auth import auth as auth_blueprint
    from .main import main as main_blueprint
    from .products import api_blueprint as product_api_blueprint,\
        view_blueprint as product_view_blueprint

    register_blueprints(app, {auth_blueprint: "/auth",
                              main_blueprint: "/",
                              product_api_blueprint: "/api/v1",
                              product_view_blueprint: "/ui"})

    return app
