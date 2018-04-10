
import os
import const

from collections import UserDict


class GoogleConfig:
    GOOGLE_LOGIN_CLIENT_ID = "1098539182056-s5n24e96ef3oquu8fbg3h40s6tl4rq2k" \
                             ".apps.googleusercontent.com"
    GOOGLE_LOGIN_CLIENT_SECRET = "0J4IG_Mr84-xFCIIm_r-xdvQ"
    GOOGLE_LOGIN_SCOPES = ['email']
    GOOGLE_LOGIN_REDIRECT_URI = "https://localhost:5000/auth/callback/google"
    GOOGLE_LOGIN_REDIRECT_SCHEME = "http"
    GOOGLE_ENDPOINTS = dict(
        scope_endpoint="https://www.googleapis.com/auth/userinfo"
    )
    GOOGLE_OPTIONS = dict(
        response_type='code',
        prompt='select_account',
        access_type='offline')


class Config(GoogleConfig):
    SECRET_KEY = "s3cr3t"
    SSL_DISABLE = False
    STATIC_DIR = const.STATIC_DIR
    TEMPLATE_DIR = const.TEMPLATE_DIR
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_MAIL_SENDER = 'BOokDB Admin <bookdb@example.com>'
    MAIL_SUBJECT_PREFIX = '[BOokDB]'

    RESULTS_PER_PAGE = 25


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(const.DATA_DIR,
                                                          "data-dev.sqlite")


class StagingConfig(Config):
    DEBUG = True


class HerokuConfig(Config):
    GOOGLE_LOGIN_REDIRECT_URI = "https://bookdb-stage.herokuapp.com/auth/callback/google"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(const.DATA_DIR,
                                                          "data-dev.sqlite")


class ConfigDict(UserDict):
    def __init__(self, default_item, *args, **kwargs):
        super(ConfigDict, self).__init__(*args, **kwargs)
        self.__default_item = default_item

    def __getitem__(self, item):
        if item not in self.keys():
            return super(ConfigDict, self).__getitem__(self.__default_item)
        return super(ConfigDict, self).__getitem__(item)


configurations = ConfigDict(
    default_item='default',
    development=DevelopmentConfig,
    stage=StagingConfig,
    default=DevelopmentConfig,
    heroku=HerokuConfig
)
