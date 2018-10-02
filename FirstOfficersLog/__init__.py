from flask import Flask
from db_controller import DBController

app = Flask(__name__, instance_relative_config=True)

db_ctl = DBController()

