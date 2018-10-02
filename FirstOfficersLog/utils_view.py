from flask import Blueprint

utils_view = Blueprint('utils_view', __name__,  url_prefix='/utils')


@utils_view.route('/')
def utils_home():
    return "Utils"

