from views import blog_view
from FirstOfficersLog import app

app.register_blueprint(blog_view)

if __name__ == '__main__':
    app.run()