from sklearn.feature_extraction.text import TfidfVectorizer
import sys, re
import numpy as np
from random import random
from operator import add
import pymongo
from pymongo import MongoClient
import string
import os

client = MongoClient()
db = client.bookdb
posts = db.posts

def process_input(input_string):
	#returns list of words in format ["$word1", "$word2", ..., "$wordn"]
	"""
	Next steps: 
	- Stem texts before putting them into the database, and then stem the query
	  input in this function to ensure that results are not thrown off by plurals, etc.
	- Remove stopwords from query input as well. scores for stopwords shouldn't mater.
	- add in some simple rules that make this smarter. i.e. cut ("books about") from queries
	"""
	input_string = input_string.translate(string.maketrans("",""), string.punctuation)
	words = input_string.split() #now a list
	for i in range(len(words)):
		new_word = "$" + words[i]
		words[i] = new_word  
	return words



def query(input_str, n_results):
	words = process_input(input_str) #returns list of words to retrieve values for in queryable format
	#mongo query. sums values of all words in query. val is 0 if not in document.
	results = posts.aggregate(
	   [
	     {
	       "$group":
	         {
	           "_id":{ "_id": "$_id", "author": "$author_id_0011", "title": "$title_id_0011" }, #features to include in output
	           "totalAmount": { "$sum": { "$sum": words}}   #format: ["$word1", "$word2", ..., "$wordn"]
	         }
	     },
	     { 
	     	"$sort": 
	     	 { 
	     		"totalAmount": -1  #sort descending
	     	 } 
	     },
	     { 
	     	"$limit" : n_results  #limit to this many results 
	     }
	   ]
	) 
	return results

#example of this in action:
out = query("the quick brown fox jumped over the lazy dog", 20)
for i in out:
	print i

