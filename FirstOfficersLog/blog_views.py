from flask import render_template, Blueprint

blog_view = Blueprint('blog_view', __name__)


# Blog view paths
@blog_view.route('/')
def home():
    """

    Returns:

    """
    return render_template('index.html')

