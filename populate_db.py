from sklearn.feature_extraction.text import TfidfVectorizer
import sys, re
import numpy as np
from random import random
from operator import add
import pymongo
from pymongo import MongoClient
import os

#initialize database
client = MongoClient()
db = client.bookdb
posts = db.posts

#load in content
#AI: do stemming before running this part. should improve results.
documents = []
docsDir = "/Users/jamesledoux/Documents/Drew2"
for book in os.listdir(docsDir):
	if not book.startswith('.'):    #pass hidden files such as .DS_STORE
		book = str(book) #file name
		with open("/Users/jamesledoux/Documents/Drew2/" + book, 'rb') as f:
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
		with open("/Users/jamesledoux/Documents/Drew2/" + book, 'rb') as f:
			content = f.read().splitlines()
		#find title and author
		for i in range(80):
			if "Title: " in content[i]:
				title = content[i][7:]
			if "Author: " in content[i]:
				author = content[i][8:]
		title_author_tuple = (title, author)
		title_author_store.append(title_author_tuple) 


#populate dict
#verify: sorting doesn't seem necessary here. can probably save time by killing that
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
		term = feature_names[pair[0]].encode('ascii', 'ignore').decode('ascii')    #encoding issues keep breaking the mongo queries
		local_word_dict[term] = pair[1]
	database[(title_author_store[i])] = local_word_dict 


for i in database.keys():
	title = i[0]
	author = i[1]
	try:
		post = {"title_id_0011": str(title), "author_id_0011": str(author)}
		words = database[i]
		post = dict(post.items() + words.items()) #faster to query if no nested dicts
		post_id = posts.insert_one(post).inserted_id
	except:
		print str(title) + ", " + str(author) + " failed"


#now populate the mongo collection
for i in database.keys():   #for doc in dictionary
	title = i[0].encode('ascii', 'ignore').decode('ascii') #trying to get around the encoding issues
	author = i[1].encode('ascii', 'ignore').decode('ascii') 
	try:
		post = {"title_id_0011": str(title), "author_id_0011": str(author)}
		words = database[i]
		post = dict(post.items() + words.items()) #combine words with title/author dict. faster to query if no nested dicts
		post_id = posts.insert_one(post).inserted_id #add record to db
	except:
		print str(title) + ", " + str(author) + " failed" #encoding issues. find a way to fix these w/o needing the exception handling.

