from pyquery import PyQuery as pq
import urllib2


def zomato():
	zomato_url = 'http://www.zomato.com/bangalore/restaurants'
	for i in xrange(1, 3):
		url = '%s?page=%s' % (zomato_url, i)
		print 'url', url
		response = urllib2.urlopen(url)
		res = response.read()
		d = pq(res)
		p = d('.result-title')
		print 'p', p
		for x in p:
			print x.attrib['href']
			zomato_subtask(x.attrib['href'])


def zomato_subtask(url):
	print 'url -> ', url
	response = urllib2.urlopen(url)
	res=response.read()
	d = pq(res)
	p = d('script')
	print '|%s|' % p[7].text
