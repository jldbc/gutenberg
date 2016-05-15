import numpy as np
import pandas as pd 
import sys
from sklearn.neighbors import NearestNeighbors

usr_title = sys.argv[1] # String input for title
usr_author = sys.argv[2] # String input for author

usr_title.rstrip('"')
usr_author.rstrip('"')

data = pd.read_csv("/Users/drewhoo/Desktop/test_output-1500-10k-150i.csv")

found = data[(data.book_name == usr_title) & (data.author == usr_author)]
found_book = found['ID']
found_book.tolist()
id_target = found_book[14]
print found_book
print id_target

data = pd.concat([data, pd.get_dummies(data['Cluster'])], axis=1)
data = pd.concat([data, pd.get_dummies(data['author'])], axis=1) 
titles = data['book_name']
data = data.drop('book_name', 1)
data = data.drop('Cluster', 1)
authors = data['author']
data = data.drop('author', 1)
data = data.drop('filename', 1)
data = data.fillna(0)

neigh = NearestNeighbors(5)
neigh = neigh.fit(data)

example = data[data['ID']==id_target]
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
print results.shape
results = results[['book_name','author']]
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
