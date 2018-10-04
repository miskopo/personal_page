from datetime import datetime as dt
from hashlib import sha256

from flask import Blueprint, request, render_template, flash, redirect, url_for
from flask_login import UserMixin, LoginManager, login_user, login_required, logout_user

from FirstOfficersLog import app
from blog_utils.md_parser import convert_to_html
from common.InvalidCredentialsException import InvalidCredentialsException
from common.UserNotInDBException import UserNotInDBException
from db_controller import DBController
from logger import logger

auth_view = Blueprint('auth_view', __name__, url_prefix='/auth')

db_ctl = DBController()

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
        username = request.form['username']
        _salt = db_ctl.obtain_salt(username)
        _password_hash = sha256(request.form['password'].encode() + _salt.encode()).hexdigest()
        db_ctl.verify_user(username, _password_hash)
    except (InvalidCredentialsException, KeyError):
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
            _password_hash = sha256(request.form['password'].encode() + _salt.encode()).hexdigest()
            db_ctl.verify_user(username, _password_hash)
        except (InvalidCredentialsException, UserNotInDBException):
            flash("Invalid username or password")
            logger.error("Invalid username or password provided")
            return render_template('login.html', invalid_login=True)
        flash("Logged in successfully")
        user = User()
        user.id = request.form['username']
        login_user(user, remember=True)
        return redirect(url_for('auth_view.add_post'))


@login_required
@auth_view.route('/add_post', methods=['GET', 'POST'])
def add_post():
    """

    :return:
    """
    if request.method == 'GET':
        return render_template('add_post.html', today_date=dt.now().date())
    elif request.method == 'POST':
        title = request.form['title']
        text = "\n".join(convert_to_html(request.form['text']))
        date = request.form['date']
        if db_ctl.insert_post(title, text, date):
            logger.debug("New post added to database")
            flash("Post inserted")
            return redirect(url_for('blog_view.home'))
        else:
            logger.error("Addition of new article failed ")
            flash("Addition failed")
            return render_template('add_post.html', today_date=dt.now().date())


@login_manager.unauthorized_handler
def unauthorized():
    """
    This function handles unauthorized attempts to access protected pages
    """
    flash("You must be logged in to view this page!")
    return redirect(url_for('home'))


@auth_view.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))
