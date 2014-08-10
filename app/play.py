import requests

url = 'http://www.opentable.com/opentables.aspx?t=rest&r=337&m=8&p=for 2&d=8/10/2014%207:00:00%20PM&scpref=100'

page = requests.get(url)
		
print page