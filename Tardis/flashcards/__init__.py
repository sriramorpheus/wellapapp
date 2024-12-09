from flask import Blueprint

flashcards_bp = Blueprint('flashcards', __name__, template_folder='templates')

from . import routes