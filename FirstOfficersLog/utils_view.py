from flask import Blueprint, render_template

utils_view = Blueprint('utils_view', __name__,  url_prefix='/utils')


@utils_view.route('/')
def utils_home():
    return render_template('index_utils.html')

