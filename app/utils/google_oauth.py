
import requests
import uuid

from functools import wraps
from urllib.parse import urljoin, parse_qsl, urlencode
from flask import current_app, redirect, request, url_for
from flask_login import LoginManager


GOOGLE_OPEN_CONFIG_URI = "https://accounts.google.com/.well-known/openid-configuration"
GOOGLE_OPEN_CONFIG = requests.get(GOOGLE_OPEN_CONFIG_URI).json()


class GoogleOAuth(object):
    _state = None

    def __init__(self, client_id, client_secret, redirect_uri, scopes,
                 authorization_endpoint=None, token_endpoint=None,
                 userinfo_endpoint=None, revocation_endpoint=None,
                 scope_endpoint=None):
        """
        :param client_id:
        :param client_secret:
        :param redirect_uri:
        :param scopes: Enum["openid", "email", "profile"]
        :param authorization_endpoint:
        :param token_endpoint:
        :param userinfo_endpoint:
        :param revocation_endpoint:
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self._scopes = scopes

        self._authorization_endpoint = self._if_none_get_other(
            GOOGLE_OPEN_CONFIG,
            'authorization_endpoint',
            authorization_endpoint)

        self._token_endpoint = self._if_none_get_other(
            GOOGLE_OPEN_CONFIG,
            'token_endpoint',
            token_endpoint)

        self._userinfo_endpoint = self._if_none_get_other(
            GOOGLE_OPEN_CONFIG,
            'userinfo_endpoint',
            userinfo_endpoint)

        self._revocation_endpoint = self._if_none_get_other(
            GOOGLE_OPEN_CONFIG,
            'revocation_endpoint',
            revocation_endpoint)

        self._scope_endpoint = scope_endpoint if scope_endpoint else \
            "https://www.googleapis.com/auth/userinfo"

    @property
    def scopes(self):
        return "+".join(["%s.%s" % (self._scope_endpoint, scope) for scope in
                        self._scopes])

    @staticmethod
    def _if_none_get_other(di, key, target):
        if target is None:
            return di.get(key)
        return target

    @property
    def state(self):
        if self._state is None:
            self._state = uuid.uuid4().hex
        return self._state

    def authorization_url(self, response_type, prompt, access_type,
                          next_url=None):
        """
        https://developers.google.com/identity/protocols/OAuth2WebServer
        :param response_type: ["code", "token", "id_token", "code token", "code id_token", "token id_token", "code token id_token", "none"]
        :param prompt: consent & select_account
        :param access_type: online or offline
        :return:
        """
        params = dict(
            response_type=response_type,
            state=self.state,
            prompt=prompt,
            client_id=self.client_id,
            scope=self.scopes,
            access_type=access_type,
            redirect_uri=self.redirect_uri
        )
        return urljoin(self._authorization_endpoint, "?" + urlencode(params))

    def exchange_code(self, code, redirect_uri):
        token = requests.post(url=self._token_endpoint,
                              data=dict(
                                  code=code,
                                  redirect_uri=redirect_uri,
                                  grant_type='authorization_code',
                                  client_id=self.client_id,
                                  client_secret=self.client_secret
                              )).json()

        if not token or token.get('error'):
            raise Exception
        return token

    def get_userinfo(self, access_token):
        userinfo = requests.get(self._userinfo_endpoint, params=dict(
            access_token=access_token,
        )).json()

        if not userinfo or userinfo.get('error'):
            raise Exception
        return userinfo

    def get_access_token(self, refresh_token):
        """
        Use a refresh token to obtain a new access token
        """

        token = requests.post(self._token_endpoint, data=dict(
            refresh_token=refresh_token,
            grant_type='refresh_token',
            client_id=self.client_id,
            client_secret=self.client_secret,
        )).json()

        if not token or token.get('error'):
            raise Exception

        return token


class GoogleOAuthManager(object):

    _goauth = None

    def __init__(self, app=None, login_manager=None):
        if login_manager:
            self.login_manager = login_manager
        else:
            self.login_manager = LoginManager()

        if app:
            self._app = app
            self.init_app(app)

    def init_app(self, app, add_context_processor=True):

        if not hasattr(app, 'login_manager'):
            self.login_manager.init_app(
                app,
                add_context_processor=add_context_processor
            )

        self.login_manager.login_message = None
        self.login_manager.needs_refresh_message = None

        self.login_manager.unauthorized_handler(self.unauthorized_callback)

    @property
    def app(self):
        return getattr(self, '_app', current_app)

    @property
    def scopes(self):
        return self.app.config.get('GOOGLE_LOGIN_SCOPES', [])

    @property
    def client_id(self):
        return self.app.config['GOOGLE_LOGIN_CLIENT_ID']

    @property
    def client_secret(self):
        return self.app.config['GOOGLE_LOGIN_CLIENT_SECRET']

    @property
    def redirect_uri(self):
        return self.app.config.get('GOOGLE_LOGIN_REDIRECT_URI')

    @property
    def redirect_scheme(self):
        return self.app.config.get('GOOGLE_LOGIN_REDIRECT_SCHEME', 'http')

    @property
    def google_urls(self):
        d = dict(authorization_endpoint=None,
                 token_endpoint=None,
                 userinfo_endpoint=None,
                 revocation_endpoint=None)
        d.update(self.app.config.get('GOOGLE_ENDPOINTS', d))
        return d

    @property
    def google_options(self):
        d = dict(response_type='code',
                 prompt='select_account',
                 access_type='offline')
        d.update(self.app.config.get('GOOGLE_OPTIONS', d))
        return d

    @property
    def oauth2(self):
        if self._goauth is None:
            self._goauth = GoogleOAuth(
                client_id=self.client_id,
                client_secret=self.client_secret,
                redirect_uri=self.redirect_uri,
                scopes=self.scopes,
                authorization_endpoint=self.google_urls['authorization_endpoint'],
                token_endpoint=self.google_urls['token_endpoint'],
                userinfo_endpoint=self.google_urls['userinfo_endpoint'],
                revocation_endpoint=self.google_urls['revocation_endpoint'],
                scope_endpoint=self.google_urls['scope_endpoint']
            )
        return self._goauth

    def login_url(self, next_url=None):
        return self.oauth2.authorization_url(
            response_type=self.google_options['response_type'],
            prompt=self.google_options['prompt'],
            access_type=self.google_options['access_type'],
            next_url=next_url)

    def unauthorized_callback(self):
        return redirect(self.login_url(next_url=request.url))

    def user_loader(self, func):
        self.login_manager.user_loader(func)

    def oauth2callback(self, view_func):
        """
        Decorator for OAuth2 callback. Calls `GoogleLogin.login` then
        passes results to `view_func`.
        """

        @wraps(view_func)
        def decorated(*args, **kwargs):
            params = {}

            code = request.args.get('code')

            # Web server flow
            if code:
                token = self.oauth2.exchange_code(
                    code,
                    url_for(
                        request.endpoint,
                        _external=True,
                        _scheme=self.redirect_scheme,
                    ),
                )
                userinfo = self.oauth2.get_userinfo(token['access_token'])
                params.update(dict(token=token, userinfo=userinfo))

            # Browser flow
            else:
                if params:
                    params.update(dict(request.args.items()))
                else:
                    return '''
                    <script>
                      window.onload = function() {
                        location.href = '?' + window.location.hash.substr(1);
                      };
                    </script>
                    '''

            return view_func(**params)

        return decorated


if __name__ == "__main__":
    goauth = GoogleOAuth(client_id="1098539182056-s5n24e96ef3oquu8fbg3h40s6tl4rq2k.apps.googleusercontent.com",
                         client_secret="0J4IG_Mr84-xFCIIm_r-xdvQ",
                         redirect_uri="http://127.0.0.1:5000/auth/callback/google",
                         userinfo_endpoint="https://www.googleapis.com/auth/userinfo",
                         scopes=['email', 'profile'])

    print(goauth.authorization_url(response_type='code', prompt='select_account',
                           access_type='offline'))
