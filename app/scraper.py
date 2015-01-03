# -*- coding: utf-8 -*-
import urlparse
import requests
from lxml import html
import json
import ast
import datetime
import grequests

def get(qstring):

    id_all = {"Marea": 31159, "Per Se": 2783, "Jean Georges": 3154, 
    "Le Bernardin": 2508, "Daniel": 337, "Eleven Madison Park": 211}

    data = ast.literal_eval(qstring.replace('%22','"').replace('%20',' '))
    tables = {}
    restaurants = []
    start_date = data["start_date"]
    end_date = data["end_date"]
    time = data["time"]
    people = data["people"]
    people = str(data["people"])[-1]
    restaurants = [data["selected"][i] for i in range(len(data["selected"]))]
    for rname in restaurants:
        rid = id_all[rname]
        tables[rname] = find_tables(rname, rid, start_date, end_date, time, people)
    return json.dumps(tables)

def find_tables(rname, rid, start_date, end_date, time, people):
   
    time = str(int(time[:-2]) + 12*(int(time[:-2])!=12)) + "%3A"
    dayofweek = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    rname = rname.replace(" ","-")
    result = []
    start_date = datetime.datetime.strptime(start_date, '%m/%d/%Y')
    end_date = datetime.datetime.strptime(end_date, '%m/%d/%Y')
    check_dates = [start_date + datetime.timedelta(i) for i in range(0,(end_date-start_date).days+1)]
    check_dates = ['%s-%s-%s' % (check_date.year, check_date.strftime('%m'), check_date.strftime('%d')) for check_date in check_dates]
    start_urls = ['http://www.opentable.com/{}?DateTime={}%20{}00&Covers={}&OnlyOffers=false&RestaurantIDs={}'.format(rname,date,time,str(people),rid) for date in check_dates]
    rs = (grequests.get(u) for u in start_urls)
    pages = grequests.map(rs)
    for page in pages:
        tree = html.fromstring(page.text)
        restaurant_exists = tree.xpath('//ul[@class="dtp-results-times list-left"]/li/a/@data-datetime')
        if restaurant_exists == []:
            continue
        times = tree.xpath('//ul[@class="dtp-results-times list-left"]/li/a/@data-datetime')
        if times == []:
            continue
        for info in times:
            table_day = info.split(' ')[0]
            table_time = info.split(' ')[1]
            table_link = 'http://www.opentable.com/{}?DateTime={}%20{}00&Covers={}&OnlyOffers=false&RestaurantIDs={}'.format(rname,table_day, table_time,str(people),rid) 
            table_day = datetime.datetime.strptime(table_day, "%Y-%m-%d").strftime("%m/%d")+" "+dayofweek[datetime.datetime.strptime(table_day, "%Y-%m-%d").weekday()]
            table_time = str(int(table_time.split(':')[0])-12 * (table_time.split(':')[0]>12))+":"+table_time.split(':')[1]+"PM"
            print table_time
            result.append(table_link + "," + table_day + " " + table_time)
    return result