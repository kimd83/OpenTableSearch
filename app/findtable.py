import datetime
import requests
import grequests
from lxml import html

def find_tables(restaurant_id, start_date, time, people, num_days):

	time = [time[:-2] + ":00:00%20" + time[len(time)-2:]]        
	# if time == "Lunch":
	# 	time = ["11:00:00%20AM", "1:30:00%20PM"]
	# if time == "Dinner":
	# 	time = ["6:00:00%20PM", "8:30:00%20PM"]


	result = []
	start_date = datetime.datetime.strptime(start_date, '%m/%d/%Y')
	check_dates = [start_date + datetime.timedelta(i) for i in range(0,int(num_days)+1)]
	check_dates = ['%s/%s/%s' % (check_date.month, check_date.day, check_date.year) for check_date in check_dates]
	start_urls = ['http://www.opentable.com/opentables.aspx?t=rest&r={}&m=8&p={}&d={}%20{}&scpref=100'.format(restaurant_id,str(people),date,t) for date in check_dates for t in time]
	rs = (grequests.get(u) for u in start_urls)
	pages = grequests.map(rs)
	for page in pages:
		tree = html.fromstring(page.text)
		restaurant_exists = tree.xpath('//table[@class="ResultsGrid"]/tr/td/ul/@id')
		if restaurant_exists == []:
			continue
		times = tree.xpath('//table[@class="ResultsGrid"]/tr/td/ul/li/@a')
		if times == []:
			continue
		for info in times:
			table_day = info.split(' ')[0][2:]
			table_time = info.split(' ')[1][:-3]
			table_ampm = info.split(' ')[2][:2]
			table_link = 'http://www.opentable.com/opentables.aspx?t=rest&r={}&m=8&p={}&d={}%20{}&scpref=100'.format(restaurant_id,str(people),table_day,table_time+":00%20"+table_ampm) 
			result.append(table_day + " " + table_time + table_ampm + " " + table_link)
	return result