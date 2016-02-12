from django.shortcuts import render
from django.http import HttpResponse, StreamingHttpResponse
from django.template import RequestContext, loader
from django.conf import settings
from django.utils.encoding import *
import urllib, urllib2
import datetime, time
import base64, hmac, hashlib, json, sys, re
from django.templatetags.static import static

#Import configurations like api key
#Requires a file config.py with an entry apikey = "<key>"
import config

# Create your views here.

#Userid lookup table
lookup_table = {}

def fetch_data(request):
	month = request.GET.get('month','').lstrip('0')
	year = request.GET.get('year','')
	projectID = request.GET.get('id','')
	billableOnly = (request.GET.get('billableOnly','')).lower()

	#url = 'https://futuhours.futurice.com/api/v1/hours/?format=json&project=341765&limit=0'
	if projectID == '':
		return HttpResponse("No projectID specified.")
	url = 'https://futuhours.futurice.com/eapi/v1/hours/?format=json&project=' + str(projectID) + '&limit=0'
	request = urllib2.Request(url, headers={"Authorization" : config.apikey})
	data = json.loads(urllib2.urlopen(request).read())

	#Remove non billable hours if parameter is set
	if billableOnly == 'true':
		data['objects'] = filter(lambda item: item['billable'] == True, data['objects'])
	output = '<table>'
	output += '<tr><th>Date</th><th>Task</th><th>User</th><th>Hours</th><th>Desc</th></tr>'
	#Remove non relevant years
	if year != '':
		data['objects'] = filter(lambda item: item['day'].split("-")[0] == year, data['objects'])
	#Remove non relevant months
	if month != '':
		data['objects'] = filter(lambda item: item['day'].split("-")[1].lstrip('0') == month, data['objects'])

	for item in data['objects']:
		output += '<tr>'
		output += '<td>' + item['day'] + '</td>' + '<td>' + item['task_name'] + '</td>' + '<td>' + fetch_user(item['user']) + '</td>' + '<td>' + str(item['hours']) + '</td>' + '<td>' + item['description'] + '</td>'
		output += '</tr>'

	output += '</table>'
	return HttpResponse(output)

def fetch_user(user_url):
	url = 'https://futuhours.futurice.com' + user_url + '?format=json'
	#Fix user url to use eapi instead of api, remove when futuhours eapi has been fixed
	url = url.replace("api","eapi")
	#Store data in local lookup table to make it blazing fast
	ints = re.findall(r'\d+', url)
	userid = ints[1]
	#Check if entry exists in lookup table
	if userid in lookup_table:
		return lookup_table[userid]
	request = urllib2.Request(url, headers={"Authorization" : config.apikey})
	data = json.loads(urllib2.urlopen(request).read())
	lookup_table[userid] = data['first_name'] + " " + data['last_name']
	return data['first_name'] + " " + data['last_name']




