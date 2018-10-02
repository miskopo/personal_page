from hashlib import sha256

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user

from FirstOfficersLog import app, db_ctl
from common.InvalidCredentialsException import InvalidCredentialsException
from common.UserNotInDBException import UserNotInDBException
from logger import logger

auth_view = Blueprint('auth_view', __name__, url_prefix='/auth')


login_manager = LoginManager()
login_manager.init_app(app)


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
        db_ctl.verify_user(**request.form)
    except InvalidCredentialsException:
        return None
    user = User()
    user.id = request.form.get('username')
    user.is_authenticated = True
    return user


@auth_view.route('/', methods=['GET', 'POST'])
def auth_home():
    if request.method == 'GET':
        logger.debug("Rendering login page")
        return render_template('login.html')
    elif request.method == 'POST':
        logger.debug("Attempting authentication")
        if not request.form['username'] or not request.form['password']:
            flash("Username and password are compulsory!")
            return render_template('login.html', invalid_login=True)
        try:
            username = request.form['username']
            _salt = db_ctl.obtain_salt(username)
            _password_hash = sha256(request.form['password'] + _salt)
            db_ctl.verify_user(username, _password_hash)
        except InvalidCredentialsException or UserNotInDBException:
            flash("Invalid username or password")
            logger.error("Invalid username or password provided")
            return render_template('login.html', invalid_login=True)
        flash("Logged in successfully")
        user = User()
        user.id = request.form['username']
        login_user(user, remember=True)
        # TODO: Finish implementation
        return "Under construction"


@login_manager.unauthorized_handler
def unauthorized():
    """
    This function handles unauthorized attempts to access protected pages
    """
    flash("You must be logged in to view this page!")
    return redirect(url_for('index'))


@auth_view.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))