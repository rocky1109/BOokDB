
from flask import Blueprint

main = Blueprint('main', __name__)

from .views import index
from .errors import internal_server_error, forbidden, page_not_found