from flask import render_template, Blueprint
from db_controller import DBController

db_ctl = DBController()

blog_view = Blueprint('blog_view', __name__)


# Blog view paths
@blog_view.route('/')
def home():
    """

    Returns:

    """
    posts = db_ctl.obtain_posts()
    return render_template('index.html', posts=posts)

