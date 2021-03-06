#!/usr/bin/python2.7
#coding:utf-8

import os
import urllib2
import requests
from dummy import *

info = {
	'NAME':'Port and Service Discover',
	'AUTHOR':'yangbh',
	'TIME':'20140707',
	'WEB':'',
	'DESCRIPTION':'端口扫描',
	'VERSION':'1.0',
	'RUNLEVEL':0
}
opts = [
	['ip','176.28.50.165','target ip'],
]
def generateUrl(ip=None,ports=None):
	''''''
	httpports = []
	for eachport in ports.keys():
		if ports[eachport]['name'] == 'http':
			httpports.append(eachport)
	# print 'httpports:\t',httpports
	logger('httpports:\t'+str(httpports))

	# url redict  hasn't been considered
	urls = []
	tmpurls = []

	if ip != None and httpports != None:
		for eachport in httpports:
			if eachport == 443:
				url = 'https://' + ip + ':' + str(eachport)
			else:
				url = 'http://' + ip + ':' + str(eachport)
			tmpurls.append(url)
	logger('tmpurls:\t'+str(tmpurls))

	for url in tmpurls:
		try:
			logger('url=%s ' % url)
			rq = requests.get(url,timeout=20,allow_redirects=True)
			if rq.status_code == 200:
				if url in rq.url:
					urls.append(url)
		except (requests.exceptions.RequestException) as e:
			logger(str(e))

	logger('urls:\t'+str(urls))

	return urls

def Assign(services):
	if services.has_key('ip'):
		return True
	return False

def Audit(services):
	logger('services=%s' % services)
	ip = services['ip']
	np = NmapScanner(ip)
	sc = np.scanPorts()
	try:
		services['ip'] = sc.keys()[0]
		services['ports'] = []
		services['port_detail'] = {}
		if sc[sc.keys()[0]].has_key('tcp'):
			services['port_detail'].update(sc[sc.keys()[0]]['tcp'])
			for eachport in sc[sc.keys()[0]]['tcp']:
				services['ports'].append(eachport)
		if sc[sc.keys()[0]].has_key('udp'):
			services['port_detail'].update(sc[sc.keys()[0]]['udp'])
			for eachport in sc[sc.keys()[0]]['udp']:
				services['ports'].append(eachport)

		services['ports'].sort()
		logger('services:%s' %services)
		security_note(str(services['ports']))
		if services.has_key('nogather') and services['nogather'] == True:
			pass
		else:
			# add sub task
			if services.has_key('mode') and services['mode']=='nogather':
				pass
			else:
				urls = generateUrl(ip,services['port_detail'])
				pprint(urls)
				for url in urls:
					add_scan_task(url)

	# except IndexError,e:
	except KeyError,e:
		logger('KeyError:%s' % str(e))
# ----------------------------------------------------------------------------------------------------
#
# ----------------------------------------------------------------------------------------------------
if __name__=='__main__':
	ip='176.28.50.165'
	if len(sys.argv) ==  2:
		ip = sys.argv[1]
	services={'ip':ip}
	print Audit(services)
	pprint(services)