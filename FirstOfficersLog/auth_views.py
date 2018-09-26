from flask import Blueprint

auth_view = Blueprint('auth_view', __name__, url_prefix='/auth')


@auth_view.route('/')
def auth_home():
    """

    Returns:

    """
    return "This area is for auth users only"
