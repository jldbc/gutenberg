from sklearn.feature_extraction.text import TfidfVectorizer
import sys, re
import numpy as np
from random import random
from operator import add
from pyspark import SparkContext, SparkConf
from pyspark.mllib.feature import HashingTF
from pyspark.mllib.feature import IDF
from pyspark.mllib.linalg import SparseVector
from pyspark.mllib.clustering import KMeans, KMeansModel
from pyspark.mllib.linalg import SparseVector
import os

sc = SparkContext(appName="Python")
docsDir = "/Users/jamesledoux/Documents/james"
#outputPath = sys.argv[2]
#print docsDir, outputPath
files = sc.wholeTextFiles(docsDir)
names = files.keys().toLocalIterator()

#should probably do some stemming, set to lowercase before or right after here 
documents = files.values()

tfidf = TfidfVectorizer(max_df=0.9,
                        ngram_range=(1, 1),
                        stop_words='english',
                        strip_accents='unicode', analyzer = 'word')

texts = documents #keep tihs separate for retrieving individual texts in title/author grabbing
documents = documents.toLocalIterator()
tfidf_matrix =  tfidf.fit_transform(documents)

feature_names = tfidf.get_feature_names() 
dense = tfidf_matrix

#get names of books and authors from files
title_author_store = []
for book in os.listdir(docsDir):
	title = None
	author = None
	#read file
	if not book.startswith('.'):    #pass hidden files such as .DS_STORE
		book = str(book)
		with open("/Users/jamesledoux/Documents/james/" + book, 'rb') as f:
			content = f.read().splitlines()
		#find title and author
		for i in range(80):
			if "Title: " in content[i]:
				title = content[i][7:]
			if "Author: " in content[i]:
				author = content[i][8:]
		title_author_tuple = (title, author)
		title_author_store.append(title_author_tuple)


#populate database
database = {}
#for i in range(len(dense)):
for i in range(dense.shape[0]):
	episode = dense[i].toarray()[0]
	phrase_scores = [pair for pair in zip(range(0, len(episode)), episode) if pair[1] > 0]
	#get top results 
	sorted_phrase_scores = sorted(phrase_scores, key=lambda t: t[1] * -1)
	#create dict of {word: score} for fast lookups
	local_word_dict = {}
	for pair in sorted_phrase_scores:
		term = feature_names[pair[0]]
		local_word_dict[term] = pair[1]
	database[(title_author_store[i])] = local_word_dict 
print "database done"


def search(term):
	"""
	for each book, locate the search term and create a tuple of (title_author_tuple, word score)
	next, sort to find top scores, print top title/author: score results for the query
	"""
	keys = database.keys()
	scores = []
	for book in keys:
		#see if it exists. equals 0 if not.
		try:
			score = database[book][term]
		except:
			score = 0
		tup = (book, score)
		scores.append(tup)
	results = sorted(scores, key=lambda x: x[1], reverse=True)  #sort on the scores
	#show top n bookid, word score pairs
	print "top results for " + str(term) + ": "
	for i in range(7):
		title = results[i][0][0]
		author = results[i][0][1]
		print str(title) + " by " + str(author) + ": " + str(results[i][1])

query = str(raw_input("Search Query: "))
search(query)

