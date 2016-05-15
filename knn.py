######################################
#			 Current Version		 #
######################################
import numpy as np
import pandas as pd 
import sys
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import MinMaxScaler
import time
# data = pd.read_csv("/Users/drewhoo/Desktop/test_output-1500-10k-150i.csv")
data = pd.read_csv("/Users/drewhoo/Desktop/all-data.csv")

# usr_title = sys.argv[1] # String input for title [DEPRECATED]
# usr_author = sys.argv[2] # String input for author [DEPRECATED]
attempts = 5
for attempt in xrange(attempts):
	try:
		usr_title = raw_input("Enter Title: ")
		usr_author = raw_input("Enter Author: ")
		# usr_title.rstrip('"')
		# usr_author.rstrip('"')
		found = data[(data.book_name == usr_title) & (data.author == usr_author)]
		found_book = found['ID']
		id_target = found_book.tolist()[0]
	except IndexError:
		# raise e('Title and Author Incorrect or Does not exist')
		print "**** Title and/or Author Incorrect or Book is not in corpus****\nPlease try again"
		# sys.exit(1)
	else:
		print "************** Searching for Book *******************"
		break
# Start timer
start_time = time.time()

# print found_book.tolist()

# found_book.tolist() #Idiot... found_book = found_book.tolist() gotta convert it
# print "Found book ID = ",found_book
# print "ID target ",id_target

# status = "**************** Adjusting Data *******************"
# print status
data = data.drop('>', 1)
data = data.drop('(', 1)
data = data.drop('[', 1)
data = data.drop('{', 1)
data = data.drop('#', 1)
data = data.drop('&', 1)
data = data.drop('/', 1)
data = data.drop('\\', 1)
data = data.drop('*', 1)
data = data.drop('@', 1)
data = data.drop('_', 1)
data = data.drop('^', 1)



# data = pd.concat([data, pd.get_dummies(data['Cluster'])], axis=1)
data = pd.concat([data, pd.get_dummies(data['smallClusterId'], prefix="general")], axis=1)  #and for each cluster
data = pd.concat([data, pd.get_dummies(data['mediumClusterId'], prefix="medium")], axis=1) 
data = pd.concat([data, pd.get_dummies(data['largeClusterId'], prefix="specific")], axis=1) 
data = pd.concat([data, pd.get_dummies(data['author'])], axis=1)  #now you have a binary variable for each author

titles = data['book_name']
authors = data['author']
IDs = data['ID']

data = data.drop('ID', 1)
data = data.drop('book_name', 1)
data = data.drop('mediumClusterId', 1)
data = data.drop('smallClusterId', 1)
data = data.drop('largeClusterId', 1)
data = data.drop('author', 1)
data = data.drop('filename', 1)
data = data.fillna(0)


scaler = MinMaxScaler()
data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
# data.to_csv("Normalized output.csv")
data['ID'] = IDs  #had to remove this earlier because we didn't want IDs to be scaled with the other columns 

print("Completed in %.3f seconds..." % (time.time() - start_time))

status = "*********** Finding Recommendations ***************"
print status
start_time = time.time()

example = data[data['ID']==id_target]
example = example.drop('ID', 1)
data = data.drop('ID', 1)


neigh = NearestNeighbors(5)
neigh = neigh.fit(data)



# print "example ", example
output = neigh.kneighbors(example, 15)
a = output[0]
b = output[1]
# print "Distance ", a
# print "Nearest Neighbor ", b
b = b.tolist()
b = b[0]

fulldata = data
fulldata['author'] = authors
fulldata['book_name'] = titles
results = data.iloc[b,:]
# print results.shape
results = results[['book_name','author']]
print("Completed in %.3f seconds..." % (time.time() - start_time))

status = "************* Your Recommendations ***************"
print status
print results

##################################################
# DEPRECATED # Saved for reference # Will Delete #
##################################################
# import numpy as np
# import pandas as pd 
# from sklearn.neighbors import NearestNeighbors

# data = pd.read_csv("/Users/drewhoo/Desktop/test_output-1500-10k-150i.csv")
# data = pd.concat([data, pd.get_dummies(data['Cluster'])], axis=1)
# data = pd.concat([data, pd.get_dummies(data['author'])], axis=1) 

# titles = data['book_name']
# data = data.drop('book_name', 1)
# data = data.drop('Cluster', 1)
# authors = data['author']
# data = data.drop('author', 1)
# data = data.drop('filename', 1)
# data = data.fillna(0)
# #data['Cluster'].get_dummies(sep='*')
# #dums = pd.get_dummies(data['Cluster'])
# #dums['id'] = data['id']
# #data = data.merge(dums, on='id')
# print data.shape
# neigh = NearestNeighbors(5)
# neigh = neigh.fit(data)

# #example = data.loc[6]
# example = data[data['ID']==210]

# output = neigh.kneighbors(example, 15)
# a = output[0]
# b = output[1]

# b = b.tolist()
# b = b[0]

# fulldata = data
# fulldata['author'] = authors
# fulldata['book_name'] = titles
# results = data.iloc[b,:]
# print results.shape
# results = results[['book_name','author']]
# print results
