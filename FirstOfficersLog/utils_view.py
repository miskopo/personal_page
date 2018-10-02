from flask import Blueprint

utils_view = Blueprint('utils_view', __name__)


@utils_view.route('/')
def index():
    return "Utils"

