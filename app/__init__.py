from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from config import config
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'password' 
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
    app.config['CSRF_ENABLED'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL'] or 'postgresql://localhost/findtable'

    db.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    print(os.environ['DATABASE_URL'])

    return app