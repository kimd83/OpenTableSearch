from flask import Flask, g
from contextlib import closing
import sqlite3
from scraper import send_alerts

DATABASE = "./opentable.db"

app = Flask(__name__)
from app import views

app.config.from_object(__name__)

def connect_db():
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

def send_alerts():
    with app.app_context():
        g.db = connect_db()
        scraper.send_alerts()

