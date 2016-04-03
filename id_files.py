from os import listdir
from os.path import isfile, join
import time

def id(path):
	start = time.clock()
	onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
	ids = {}
	x = 0
	for file in onlyfiles:
		if file.endswith(".txt"):
			file = file.replace('.txt', '').split('___')
			ids[x+1] = file
			x += 1
	end = time.clock()
	print "This took: ", (end - start)
	print ids

"""
How do we want to format this "table"
Do we make a dictionary for efficient lookup? {ID : [Author, title]}
def id(path):
	onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
	file_list = []
	ids = {}
	for file in onlyfiles:
		if file.endswith(".txt"):
			file = file.split('___')
			file_list.append(file)
	for x in range(len(file_list)):
		ids[x+1] = file_list[x]
	print ids
"""