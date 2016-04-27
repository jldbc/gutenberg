import xml.etree.ElementTree as ET
import requests
import urllib2
from clean_from_web import strip_headers

def get_URLs():
	############ Enter your filepath here ############
	filepath = '/Users/drewhoo/Desktop/cache/epub'

	filename = ['/Users/drewhoo/Desktop/cache/epub/26/pg26.rdf', '/Users/drewhoo/Desktop/cache/epub/27/pg27.rdf', '/Users/drewhoo/Desktop/cache/epub/28/pg28.rdf']

	urls = []
	limit = 51837
	limit_small = 100
	files = []
	file_lang = []
	# for x in range(limit):
	for x in range(limit_small):
		file = filepath + "/" +  str(x) + "/pg" + str(x) + ".rdf"
		#print file
		files.append(file)

	for file in files:
		rdf = open(file).read()
		#tree = etree.fromstring(rdf)
		tree = ET.parse(file)
		root = tree.getroot()
		listURLs = []
################################################
		# for country in root.findall('country'):
		# 	rank = country.find('rank').text
		# 	name = country.get('name')
		# 	print name, rank
################################################
		# l = root.find('datatype="http://purl.org/dc/terms/RFC4646"').text
################################################
		# l = root.find('{http://purl.org/dc/terms/RFC4646}hasFormat')
		# print "Lang = ", l

		#   # for thing in child:
		#   #   if thing.tag == "{http://purl.org/dc/terms/RFC4646}hasFormat":
		#   #   	for something in thing:
		#   #   		print "Lang: ", something.attrib

		for child in root:
		  for thing in child:
		    if thing.tag == "{http://purl.org/dc/terms/}hasFormat":
		      for something in thing:
		      	if "utf-8" in something.attrib.values()[0]:
		      		urls.append(something.attrib.values()[0])
		        #listURLs.append(something.attrib.values()[0])
		##########################################
		# Deprecated
		# Look at each element of listURLs to find substring
		# for i in range(len(listURLs)):
		# 	if "utf-8" in listURLs[i]:
		# 		urls.append(listURLs[i])
		##########################################
	#print "These are the urls: \n", urls
		# print listURLs
		# print "\nfile Lang: ", file_lang
	print urls
	return urls

def retrieve_file():
	urls = get_URLs()
	
	# for line in data:
	#     print line
	for x in range(5):
		num = 5 + x
		#data = urllib2.urlopen(urls[num])
		data = requests.get(urls[num])
		data = strip_headers(data)
		file_name = "Output_" + str(x) + ".txt"
		with open(file_name, "w") as file:
			for line in data:
				file.write(line)

#get_URLs()
retrieve_file()
