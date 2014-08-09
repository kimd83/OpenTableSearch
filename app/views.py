from flask import request, render_template
from app import app


@app.route('/')
@app.route('/index')
def index():
	return render_template("index.html")


@app.route('/findtable', methods=['GET', 'POST'])
def findtable():
	if request.method == 'POST':
		# start_date = request.form['start_date']
		# time = request.form['time']
		people = request.form['people']
		# num_days = request.form['num_days']
		# rtype = request.form['rtype']
		test_string = str(people)

		return render_template("findtable.html", form = test_string)
	if request.method == 'GET':
		return render_template("findtable.html")