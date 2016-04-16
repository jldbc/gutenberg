from os import listdir
from os.path import isfile, join
import time
import pandas as pd

cluster_data = pd.read_csv("/Users/drewhoo/Desktop/Big_Data_Spark/gutenberg/clusterMembership.csv")

def get_ids():
	start = time.clock()
	path = "/Users/drewhoo/Desktop/Big_Data_Spark/gutenberg_working_copy/txt_copy"
	onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
	ids = {}
	x = 0
	for file in onlyfiles:
		if file.endswith(".txt"):
			file = file.replace('.txt', '').split('___')
			ids[x+1] = file
			x += 1
	return ids
	"""
	cluster_output_path = ""
    with open(cluster_output_path, "r") as f:
        for line in f:
            line = line.rstrip('\n')
            book_ID = line.split(',')[0] 
            book_title = ids[book_ID]

            if (line.split(',')[2] > maxValue):
                maxValue = line.split(',')[2]
            temp = float(line.split(',')[2])
            if (temp < minValue):
                minValue = temp
        subtractValue = float(maxValue) - float(minValue)
    """
    """
	end = time.clock()
	print "This took: ", (end - start)
	print ids
	"""
ids = get_ids() 

cluster_data['names'] = cluster_data['0'].map(ids)
#output_path_directory = "/Users/drewhoo/Desktop/Big_Data_Spark/gutenberg"
cluster_data.to_csv("/Users/drewhoo/Desktop/Big_Data_Spark/gutenberg/cluster_membership_with_names.csv")
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