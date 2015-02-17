from flask import request, session, url_for, current_app, render_template, Response, redirect, flash
from .. import db
from . import scraper
from ..models import Restaurant, Alert
from . import main
import re


@main.route('/', methods=['GET'])
def index():
    if request.method == 'GET':
        scraper.send_alerts()
        restaurants = Restaurant.query.order_by(Restaurant.name.desc()).all()
        return render_template("opentable.html", restaurants = restaurants)


@main.route('/scrape')
def scrape():
    reply = scraper.get(request.query_string)
    return Response(reply, status=200)


@main.route('/opentable', methods=['GET'])
def opentable():
    if request.method == 'GET':
        restaurants = Restaurant.query.order_by(Restaurant.name.desc()).all()
        return render_template("opentable.html", restaurants = restaurants)


@main.route('/help', methods=['GET'])
def help():
    if request.method == 'GET':
        return render_template("help.html")


@main.route('/alerts', methods=['GET','POST'])
def alerts():
    restaurants = Restaurant.query.order_by(Restaurant.name.asc()).all()
    if request.method == 'POST':
        session['redirected'] = True
        email = request.form['email']
        try:
            rname = request.form['rname']
        except:
            rname = ""
        if valid_email(email) & bool(rname):
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            start_time = request.form['start_time']
            end_time = request.form['end_time']
            people = request.form['people']
            status = 'active'
            rid = Restaurant.query.filter_by(name=rname).first()
            alert = Alert(restaurant = rid, start_date = start_date, end_date = end_date, start_time = start_time, end_time = end_time, people = people, email = email, status=status)     
            db.session.add(alert)
            db.session.commit()
            confirmation = "An email will be sent to " + email + " when your table becomes available!"
            table = "Your Table: " + rname + " from " + start_date + " to " + end_date + " between " + start_time + " and " + end_time + " " + people
            flash(confirmation)
            flash(table)
            return redirect(url_for('main.alerts'))
        else:
            error = "Please pick a restaurant and/or enter a valid email address"
            flash(error)
            return redirect(url_for('main.alerts'))

    return render_template("alerts.html", restaurants = restaurants)

@main.route('/alerts_active')
def alerts_active():
    alerts = Alert.query.filter_by(status='active').all()
    display_alerts = []
    for alert in alerts:
        display_alerts.append([alert.email, alert.restaurant, alert.start_date, alert.end_date, alert.start_time, alert.end_time, alert.people, alert.status])
    return render_template("show_alerts.html", alerts= display_alerts)


@main.route('/alerts_all')
def alerts_all():
    alerts = Alert.query.all()
    display_alerts = []
    for alert in alerts:
        display_alerts.append([alert.email, alert.restaurant, alert.start_date, alert.end_date, alert.start_time, alert.end_time, alert.people, alert.status])
    return render_template("show_alerts.html", alerts= display_alerts)


@main.route('/add_new', methods=['GET','POST'])
def add_new():
    if request.method == 'POST':
        rname = request.form['rname']
        rid = request.form['rid']
        restaurant = Restaurant(name=rname, opentable_id = rid)
        db.session.add(restaurant)
        db.session.commit()
        msg = rname + " has been added to the list."
        flash(msg)
        return redirect(url_for('main.add_new'))
    return render_template("add_new.html")


def valid_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    return True
