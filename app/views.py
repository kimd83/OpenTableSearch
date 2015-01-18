from flask import request, render_template, Response, g
from app import app
import scraper
import re

@app.route('/', methods=['GET'])
def main():
    if request.method == 'GET':
        scraper.send_alerts()
    return render_template("opentable.html")

@app.route('/scrape')
def scrape():
    reply = scraper.get(request.query_string)
    return Response(reply, status=200)

@app.route('/opentable', methods=['GET'])
def opentable():
    if request.method == 'GET':
        return render_template("opentable.html")

@app.route('/help', methods=['GET'])
def help():
    if request.method == 'GET':
        return render_template("help.html")

@app.route('/alerts', methods=['GET','POST'])
def alerts():
    if request.method == 'GET':
        return render_template("alerts.html")
    if request.method == 'POST':
        email = request.form['email']
        if valid_email(email):
            rname = request.form['rname']
            start_date = request.form['start_date']
            end_date = request.form['end_date']
            start_time = request.form['start_time']
            end_time = request.form['end_time']
            people = request.form['people']
            scraper.alerts(rname, start_date, end_date, start_time, end_time, people, email)
            confirmation = "An email will be sent to " + email + " when your table becomes available!"
            table = "Your Table: " + rname + " from " + start_date + " to " + end_date + " between " + start_time + " and " + end_time + " " + people
            return render_template("alerts.html", confirmation = confirmation, table = table)
        else:
            return render_template("alerts.html", confirmation = "Please enter a valid email address")

@app.route('/alerts_active')
def alerts_active():
    return render_template("show_alerts.html", alerts= scraper.show_alerts(['active']))

@app.route('/alerts_all')
def alerts_all():
    return render_template("show_alerts.html", alerts= scraper.show_alerts(['active','expired','sent']))



def valid_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return False
    return True
