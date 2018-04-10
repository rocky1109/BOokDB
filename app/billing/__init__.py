
from flask import Blueprint

view_blueprint = Blueprint('ui-billings', __name__)


from . import views
