#!.virtualenvs/findtable/bin/python

source .virtualenvs/findtable/bin/activate
cd ~/Projects/flask/portfolio
python -c 'from app import send_alerts; send_alerts()'