from flask import Blueprint
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user

from db_controller import DBController
from common.InvalidCredentialsException import InvalidCredentialsException

auth_view = Blueprint('auth_view', __name__, url_prefix='/auth')


login_manager = LoginManager()
login_manager.init_app(auth_view)


class User(UserMixin):
    pass


@login_manager.user_loader
def user_loader(username):
    user = User()
    user.id = username
    return user


@login_manager.request_loader
def request_loader(request):
    try:
        db_ctl = DBController()
        db_ctl.verify_user(**request.form)
    except InvalidCredentialsException:
        return None
    user = User()
    user.id = request.form.get('username')
    user.is_authenticated = True
    return user


@auth_view.route('/')
def auth_home():
    """

    Returns:

    """
    return "This area is for auth users only"
