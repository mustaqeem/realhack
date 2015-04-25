from pyquery import PyQuery as pq
import urllib2
from pymongo import MongoClient


def zomato():
	zomato_url = 'http://www.zomato.com/bangalore/restaurants'
	for i in xrange(1, 21):
		url = '%s?page=%s' % (zomato_url, i)
		# print 'url', url
		response = urllib2.urlopen(url)
		res = response.read()
		d = pq(res)
		p = d('.result-title')
		for x in p:
			# print x.attrib['href']
			zomato_subtask(x.attrib['href'])


def zomato_subtask(url):
	try:
		print
		print 'url -> ', url
		response = urllib2.urlopen(url)
		res=response.read()
		d = pq(res)
		p = d('script')
		print 'p[7].text', p[7].text
		geolocation = [float(x.split(':')[1].strip()) for x in p[7].text.strip().split('=')[1].strip().replace('{', '').replace('}', '').replace(';', '').split(',')]
		geolocation.reverse()
		print 'geolocation', geolocation
		p = d('.res-main-address-text')
		address = p.text()
		print 'address', address
		p = d('.res-info-cuisines')
		cuisines = p.text()
		for x in cuisines.split(','):
			storeData('food', geolocation, x)
	except Exception as ex:
		print ex


def storeData(tag_type, locn, tag):
	conn = MongoClient()
	coll = conn['feed']['feeds']
	query = {"type": tag_type, "location": locn, "tag": tag.strip().lower()}
	update = {'$inc': {'weight': 1}}
	coll.find_and_modify(query=query, update=update, upsert=True)
