from sklearn.feature_extraction.text import TfidfVectorizer
import sys, re
import numpy as np
from random import random
from operator import add
import pymongo
from pymongo import MongoClient
import os

client = MongoClient()
db = client.bookdb
posts = db.posts

def query(term, n_results):
	results = posts.find({}).sort(term, -1).limit(n_results) #pull all, sort by term, limit to top n results
	return results

out = query("dog", 20)
for i in out:
	try:
    	a = i['dog']
    	b = i['author_id_0011']
    	c = i['title_id_0011']
    except:
    	a = "0"   #equals zero if term not in book
    	b = i['author_id_0011']
    	c = i['title_id_0011']
    print c + " | " + b + " | " + str(a)