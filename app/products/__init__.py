
from flask import Blueprint

api_blueprint = Blueprint('products', __name__)
view_blueprint = Blueprint('ui-products', __name__)


from . import views, api
