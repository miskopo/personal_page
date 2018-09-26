from flask import render_template

from FirstOfficersLog import app
from auth_views import auth_view
from blog_views import blog_view

app.register_blueprint(blog_view)
app.register_blueprint(auth_view)
# logger = getLogger(__name__)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


if __name__ == '__main__':
    app.run(debug=True)
