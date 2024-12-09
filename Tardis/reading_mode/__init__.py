from flask import Blueprint

reading_mode_bp = Blueprint('reading_mode', __name__, template_folder='templates')

from . import routes
