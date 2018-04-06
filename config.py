
import os
import const

from collections import UserDict


class GoogleConfig:
    GOOGLE_LOGIN_CLIENT_ID = "1098539182056-s5n24e96ef3oquu8fbg3h40s6tl4rq2k" \
                             ".apps.googleusercontent.com"
    GOOGLE_LOGIN_CLIENT_SECRET = "0J4IG_Mr84-xFCIIm_r-xdvQ"
    GOOGLE_LOGIN_SCOPES = ['email']
    GOOGLE_LOGIN_REDIRECT_URI = "http://localhost:5000/auth/callback/google"
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
    STATIC_DIR = const.STATIC_DIR
    TEMPLATE_DIR = const.TEMPLATE_DIR
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    RESULTS_PER_PAGE = 25


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(const.DATA_DIR,
                                                          "data-dev.sqlite")


class StagingConfig(Config):
    DEBUG = True


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
    default=DevelopmentConfig
)
