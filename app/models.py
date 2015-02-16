from . import db

class Alert(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.Integer, db.ForeignKey('restaurants.id'))
    start_date = db.Column(db.String(64))
    end_date = db.Column(db.String(64))
    start_time = db.Column(db.String(64))
    end_time = db.Column(db.String(64))
    people = db.Column(db.String(64))
    email = db.Column(db.String(64))
    status = db.Column(db.String(64))

    def __repr__(self):
        return '<Alert %r>' % self.email


class Restaurant(db.Model):
    __tablename__ = 'restaurants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    opentable_id = db.Column(db.Integer, unique=True)
    alerts = db.relationship('Alert', backref='restaurant', lazy= "dynamic")

    def __repr__(self):
        return '<Restaurant %r>' % self.name
