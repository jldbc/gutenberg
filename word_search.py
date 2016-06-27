from sklearn.feature_extraction.text import TfidfVectorizer
import sys, re
import numpy as np
from random import random
from operator import add
import os

#load in content
#should probably do some stemming here
documents = []
docsDir = "/Users/jamesledoux/Documents/james"
for book in os.listdir(docsDir):
	if not book.startswith('.'):    #pass hidden files such as .DS_STORE
		book = str(book) #file name
		with open("/Users/jamesledoux/Documents/james/" + book, 'rb') as f:
			content = f.read() #.splitlines()
			content = unicode(content, errors='replace')
			documents.append(content)


tfidf = TfidfVectorizer(max_df=0.9,
                        ngram_range=(1, 1),
                        stop_words='english',
                        strip_accents='unicode', analyzer = 'word')

#documents = documents.toLocalIterator()
tfidf_matrix =  tfidf.fit_transform(documents)

feature_names = tfidf.get_feature_names() 

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
for i in range(tfidf_matrix.shape[0]):
	doc = tfidf_matrix[i].toarray()[0]
	#currently using 1-grams, but potential for use of n-grams with phrases here
	phrase_scores = [pair for pair in zip(range(0, len(doc)), doc) if pair[1] > 0]
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

query = str(raw_input("Search Query (no quotes please): ")).lower()
search(query)

