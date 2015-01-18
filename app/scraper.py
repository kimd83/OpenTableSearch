# -*- coding: utf-8 -*-
from lxml import html
import json
import ast
from datetime import datetime, date, timedelta
import grequests
from collections import OrderedDict
from flask import request, render_template, Response, g
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

dayofweek = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
id_all = {"Marea": 31159, "Per Se": 2783, "Jean Georges": 3154, 
    "Le Bernardin": 2508, "Daniel": 337, "Eleven Madison Park": 211,
    "Gramercy Tavern": 942, "Sushi Nakazawa-Sushi Bar": 118903, "Betony": 78406,
    "Carbone": 104293, "Dirty French": 151027}

def get(qstring):
    data = ast.literal_eval(qstring.replace('%22','"').replace('%20',' '))
    tables = {}
    start_date = data["start_date"]
    end_date = data["end_date"]
    start_time = data["start_time"]
    end_time = data["end_time"]
    people = data["people"]
    restaurants = [data["selected"][i] for i in range(len(data["selected"]))]
    for rname in restaurants:
        rid = id_all[rname]
        tables[rname] = find_tables(rname, rid, start_date, end_date, start_time, end_time, people)
    return json.dumps(tables)

def find_tables(rname, rid, start_date, end_date, start_time, end_time, people):
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
    urls = ['http://www.opentable.com/{}?DateTime={}%20{}&Covers={}&OnlyOffers=false&RestaurantIDs={}'.format(rname,date,time,str(people),rid) for date in check_dates for time in times]
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
            if int(table_time.split(':')[0]) < int(start_time[:-2])+ 12:
                continue
            if int(table_time.split(':')[0]) > int(end_time[:-2]) + 12:
                if table_time.split(':')[1] != '00':
                    continue
            table_link = 'http://www.opentable.com/{}?DateTime={}%20{}00&Covers={}&OnlyOffers=false&RestaurantIDs={}'.format(rname,table_day, table_time,str(people),rid) 
            table_day = datetime.strptime(table_day, "%Y-%m-%d").strftime("%m/%d")+" "+dayofweek[datetime.strptime(table_day, "%Y-%m-%d").weekday()]
            table_time = str(int(table_time.split(':')[0])- (12 * (int(table_time.split(':')[0])>12)))+":"+table_time.split(':')[1]+"PM"
            result.append(table_link + "," + table_day + " " + table_time)
    return list(OrderedDict.fromkeys(result))

def alerts(rname, start_date, end_date, start_time, end_time, people, email):
    rid = id_all[rname] 
    status = "active"      
    g.db.execute('insert into alerts (rname, rid, start_date, end_date, start_time, end_time, people, email, status) values (?,?,?,?,?,?,?,?,?)', [rname, rid, start_date, end_date, start_time, end_time, people, email, status])
    g.db.commit()

def show_alerts(status):
    cur = g.db.execute("SELECT alert_id, rname, start_date, end_date, start_time, end_time, people, email, status from alerts where status in (%s) order by alert_id desc" % ', '.join('?' * len(status)), status)
    alerts = [dict(alert_id=row[0], rname=row[1], start_date=row[2], end_date=row[3], start_time=row[4], end_time=row[5], people=row[6], email=row[7], status=row[8]) for row in cur.fetchall()]
    result = []
    for alert in alerts:
        result.append((alert['alert_id'], alert['email'], alert['rname'], alert['start_date'], alert['end_date'], alert['start_time'], alert['end_time'], alert['people'], alert['status']))
    return result

def send_alerts():
    cur = g.db.execute("SELECT alert_id, rname, start_date, end_date, start_time, end_time, people, email, status from alerts order by alert_id desc")
    alerts = [dict(alert_id=row[0], rname=row[1], start_date=row[2], end_date=row[3], start_time=row[4], end_time=row[5], people=row[6], email=row[7], status=row[8]) for row in cur.fetchall()]
    for alert in alerts:
        if alert['status'] != 'active':
            continue
        else:
            alert_id = alert['alert_id']
            if datetime.strptime(alert['end_date'],"%m/%d/%Y") < datetime.today():
                g.db.execute("UPDATE alerts SET status = 'expired' WHERE alert_id = ?", (alert_id,))
            else:
                table = find_tables(alert['rname'], id_all[alert['rname']], alert['start_date'], alert['end_date'], alert['start_time'], alert['end_time'], alert['people'])
                if table:
                    SUBJECT = 'We found a table for you!'
                    FROM = 'opentablesearch@gmail.com'
                    TO = [alert['email']]
                    TEXT = "There is a table at " + alert['rname'] + " " + alert['people'] + " on " + table[0].split(",")[-1] + "\n" +table[0].split(",")[0]
                    message = "\From: %s\nTo: %s\nSubject: %s\n\n%s" % (FROM, TO, SUBJECT, TEXT)
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    server.login('opentablesearch@gmail.com','searchtable')
                    server.sendmail(FROM, TO, message)
                    server.close()
                    g.db.execute("UPDATE alerts SET status = 'sent' WHERE alert_id = ?", (alert_id,))
                    g.db.commit()
    return 0









