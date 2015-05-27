from flask import Blueprint

general = Blueprint('general', __name__)

from . import views, errors