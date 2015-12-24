# -*- coding: utf-8 -*-
from lxml import html
import json
import ast
from datetime import datetime, date, timedelta
import grequests
from collections import OrderedDict
from flask import request, render_template, Response
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from ..models import Restaurant, Alert
from .. import db

dayofweek = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

def get(qstring):
    data = ast.literal_eval(qstring.decode("utf-8").replace('%22','"').replace('%20',' '))
    tables = {}
    start_date = data["start_date"]
    end_date = data["end_date"]
    start_time = data["start_time"]
    end_time = data["end_time"]
    people = data["people"]
    restaurants = [data["selected"][i] for i in range(len(data["selected"]))]
    for rname in restaurants:
        opentable_id = Restaurant.query.filter_by(name=rname).first().opentable_id
        tables[rname] = find_tables(rname, opentable_id, start_date, end_date, start_time, end_time, people)
    return json.dumps(tables)

def find_tables(rname, opentable_id, start_date, end_date, start_time, end_time, people):
    people = str(people)[-1]    
    if start_time == "12PM":
        start_time = "0PM"
    if end_time == "12PM":
        end_time = "0PM"
    times = range(int(start_time[:-2]), int(end_time[:-2]))
    times = [str(time + 12) + "%3A30" for time in times]
    rname = rname.replace(" ","-")
    start_date = datetime.strptime(start_date, '%m/%d/%Y')
    end_date = datetime.strptime(end_date, '%m/%d/%Y')
    check_dates = [start_date + timedelta(i) for i in range(0,(end_date-start_date).days+1)]
    check_dates = ['%s-%s-%s' % (check_date.year, check_date.strftime('%m'), check_date.strftime('%d')) for check_date in check_dates]
    urls = ['http://www.opentable.com/{}?DateTime={}%20{}&Covers={}&OnlyOffers=false&RestaurantIDs={}'.format(rname,date,time,str(people),opentable_id) for date in check_dates for time in times]
    requests = (grequests.get(u) for u in urls)
    pages = grequests.map(requests)
    result = []
    for page in pages:
        tree = html.fromstring(page.text)
        tables = tree.xpath('//ul[@class="dtp-results-times list-left"]/li/a/@data-datetime')
        if tables == []:
            continue
        for table in tables:
            table_day = table.split(' ')[0]
            table_time = table.split(' ')[1]
             #exclude tables outside of (start_time, end_time)
            if int(table_time.split(':')[0]) < int(start_time[:-2]) + 12:
                continue
            if int(table_time.split(':')[0]) > int(end_time[:-2]) + 12:
                continue
            if int(table_time.split(':')[0]) == int(end_time[:-2]) + 12:
                if table_time.split(':')[1] != '00':
                    continue
            table_link = 'http://www.opentable.com/{}?DateTime={}%20{}00&Covers={}&OnlyOffers=false&RestaurantIDs={}'.format(rname,table_day, table_time,str(people),opentable_id) 
            table_day = datetime.strptime(table_day, "%Y-%m-%d").strftime("%m/%d")+" "+dayofweek[datetime.strptime(table_day, "%Y-%m-%d").weekday()]
            table_time = str(int(table_time.split(':')[0])- (12 * (int(table_time.split(':')[0])>12)))+":"+table_time.split(':')[1]+"PM"
            result.append(table_link + "," + table_day + " " + table_time)
    return list(OrderedDict.fromkeys(result))

def send_alerts():
    alerts = Alert.query.all()
    for alert in alerts:
        if alert.status != 'active':
            continue
        else:
            if datetime.strptime(alert.end_date,"%m/%d/%Y") < datetime.today():
                alert.status = 'expired'
            else:
                rid = alert.rid
                rname = Restaurant.query.filter_by(id = rid).first().name
                opentable_id = Restaurant.query.filter_by(id = rid).first().opentable_id
                table = find_tables(rname, opentable_id, alert.start_date, alert.end_date, alert.start_time, alert.end_time, alert.people)
                if table:
                    alert.status = 'sent'
                    SUBJECT = 'We found a table for you!'
                    FROM = 'opentablesearch@gmail.com'
                    TO = [alert.email]
                    TEXT = "There is a table at " + rname + " " + alert.people + " on " + table[0].split(",")[-1] + "\n" +table[0].split(",")[0]
                    message = "\From: %s\nTo: %s\nSubject: %s\n\n%s" % (FROM, TO, SUBJECT, TEXT)
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    server.login('opentablesearch@gmail.com','tablesearch')
                    server.sendmail(FROM, TO, message)
                    server.close()
    db.session.commit()
    return 0









