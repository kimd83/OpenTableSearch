from app import db

class Restaurant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    r_name = db.Column(db.String(80), unique=True)
    r_code = db.Column(db.Integer, unique=True)

class Alert(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    r_name = db.Column(db.String(80), ForeignKey('Restaurant.r_name'))
    start_date = db.Column(db.String(80))
    end_date = db.Column(db.String(80))
    start_time = db.Column(db.String(80))
    end_time = db.Column(db.String(80))
    people = db.Column(db.String(80))
    email = db.Column(db.String(80))
    status = db.Column(db.String(80))







