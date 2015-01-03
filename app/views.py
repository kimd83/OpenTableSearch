from flask import request, render_template, Response
from app import app
import scraper

@app.route("/scrape")
def scrape():
    reply = scraper.get(request.query_string)
    return Response(reply, status=200)

@app.route('/opentable', methods=['GET', 'POST'])
def opentable():
    if request.method == 'GET':
        return render_template("opentable.html")

@app.route('/help', methods=['GET'])
def help():
    if request.method == 'GET':
        return render_template("help.html")

