import numpy as np
import pandas as pd 
from sklearn.neighbors import NearestNeighbors

data = pd.read_csv('/Users/jamesledoux/Desktop/final_data.csv')

titles = data['book_name']
data = data.drop('book_name', 1)

data['cluster_membership'].get_dummies(sep='*')
dums = pd.get_dummies(data['cluster_membership'])
dums['id'] = data['id']
data = data.merge(dums, on='id')

neigh = NearestNeighbors(5)
neigh.fit(data)

example = data.loc[6]
output = neigh.kneighbors(example, 15)
a = output[0]
b = output[1]

neigh.fit(X, y) 



