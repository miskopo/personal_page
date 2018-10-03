from flask import Flask

app = Flask(__name__, instance_relative_config=True)

app.secret_key = '28B87E35G9D5GAF7655B8111A8642'
