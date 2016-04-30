from __future__ import division
from nltk.stem.snowball import *
from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
from nltk import tokenize
import numpy as np
import pandas as pd
import string
import csv
import sys
from datetime import datetime
import os

startTime = datetime.now()
#need this or else it throws encoding/decoding errors
reload(sys)
sys.setdefaultencoding('utf8')
punct = set(['!', '#', '"', '%', '$', '&', ')', '(', '+', '*', '-', ',', '/', '.', ';', ':', '=', '<', '?', '>', '@', '[', ']', '\\', '_', '^', '`', '{', '}', '~'])
table = string.maketrans("","")
target = open("output.txt", 'w')

#check avg sent size
target.write("book_name|total_words|avg_sentence_size|!|#|''|%|$|&|')'|(|+|*|-|,|/|.|;|:|=|<|?|>|@|[|]|\|_|^|`|{|}|~|neg|neu|pos|compound|ID|")
target.write('\n')

def ensure_unicode(v):
    #if isinstance(v, str):
    v = v.decode('utf-8', errors='ignore')
    #return unicode(v)
    return v

def punctAndWordsInSentence(listOfCharacters):
    punctuation_dict = {}
    sentenceCounter = 0;
    wordCounter = 0
    periodCounter = 0;
    avgSentenceSize = 0;
    totalWords = 0;
    punctCounter = 0;
    """
    Iterate through all characters. Count periods, punct frequencies. WordCounter = words in sentence (resets
    to zero after a period). totalWords is the book's total word count.
    """
    for i in listOfCharacters:
        if i == ' ':
            wordCounter = wordCounter + 1
        if i == '.':
            periodCounter = periodCounter + 1
            totalWords = totalWords + wordCounter
            wordCounter = 0
        if i in punct:
            punctCounter = punctCounter + 1
            if i in punctuation_dict:
                punctuation_dict[i] = punctuation_dict[i]+1
            else:
                punctuation_dict[i] = 1
    avgSentenceSize = (totalWords/periodCounter)
    #put together output, bar delimited
    target.write(str(totalWords) + "|")
    target.write(str(avgSentenceSize) + "|")
    s = ""
    for i in punct:
        if i in punctuation_dict:
            s = s + str(punctuation_dict[i] / punctCounter) + "|"    #pct of punct that is [x]
        else:
            s = s + str(0) + "|"                                     #0 if unused
    target.write(s)


def decode_file(text):
    return text.decode('utf-8', errors='replace')

def get_sentiment(temp):
    #data['sentiment_negative'] = 999999
    #data['sentiment_neutral'] = -999999
    #data['sentiment_positive'] = -999999
    #data['sentiment_compound'] = 0
    #data['ID'] = -999999
    temp = temp.replace('\n', '')
    temp = temp.replace('\r', '')
    content = decode_file(temp)
    content = tokenize.sent_tokenize(content)
    sid = SentimentIntensityAnalyzer()
    booksent = []
    for sentence in content:
        ss = sid.polarity_scores(sentence)
        ssarray = [ss['neg'],ss['neu'],ss['pos'], ss['compound']]
        booksent.append(ssarray)
    valuearray = np.array(booksent)
    # mean negative, neutral, positive, compound score for all lines in book
    values = np.mean(valuearray, axis=0)
    #print " "
    #print "Sentiment scores for book " #+ str(counter) + ": " + str(book)
    #print "neg: " + str(values[0]) + "  neu: " + str(values[1]) + "  pos: " + str(values[2]) + "  compound: " + str(values[3])
    return values

    #with open("sentiments/" + book[:-4] + ".csv", 'w') as f:
    #    f.write(str(values[0]) + ", " + str(values[1]) + ", " + str(values[2]) + ", " + str(values[3]))
    #f.close()

    #data.to_csv('/Users/jamesledoux/Documents/BigData/gutenberg/output.csv')


def preprocessing():
    '''
    read file as a list of words
    set lowercase, stem, remove stopwords
    get punctuation string for later feature extraction
    save local wordcount dict
    save global word dict after finished looping through docs
    '''
    counter = 0
    for book in os.listdir("/Users/jamesledoux/Downloads/txt"):
        if not book.startswith('.'):    #pass hidden files such as .DS_STORE
            book = str(book)
            with open("/Users/jamesledoux/Downloads/txt/" + book, 'rb') as f:
                content = f.read().rstrip('\n')
            target.write(book + "|")
            punctAndWordsInSentence(content)
            sentiment_values = get_sentiment(content)
            neg = sentiment_values[0]
            neu = sentiment_values[1]
            pos = sentiment_values[2]
            compound = sentiment_values[3]
            target.write(str(neg) + "|" + str(neu) + "|" + str(pos) + "|" + str(compound) + "|" + str(counter) + "|")
            content = content.translate(table, string.punctuation)
            content = ensure_unicode(content)
            content = content.decode("utf-8")
            content = content.split()
            target.write('\n')
            f.close()
            counter += 1
            if counter%100 == 0:
                print counter
            #print "book " + str(counter) + " done: " + book

preprocessing()
print datetime.now() - startTime

