from views import blog_view
from logging import getLogger
from FirstOfficersLog import app

# app.register_blueprint(blog_view)

# logger = getLogger(__name__)


@app.route('/')
def home():
    return "I work"


if __name__ == '__main__':
    app.run(debug=True)
