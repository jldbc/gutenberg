from __future__ import division
from nltk.stem.snowball import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
from nltk import tokenize
from datetime import datetime
import numpy as np
import string
import csv
import sys
import os

startTime = datetime.now()
#need this or else it throws encoding/decoding errors
reload(sys)
sys.setdefaultencoding('utf8')
punct = set(['!', '#', '"', '%', '$', '&', '(', '+', '*', '-', ',', '/', '.', ';', ':', '=', '<', '?', '>', '@', '[', ']', '_', '^', '`', '{', '~'])
table = string.maketrans("","")
target = open("output.txt", 'w')

#check avg sent size
target.write("book_name|total_words|avg_sentence_size|!|#|''|%|$|&|')'|(|+|*|-|,|/|.|;|:|=|<|?|>|@|[|]|\|_|^|`|{|}|~|neg|neu|pos|compound|ID|Title|Author|")
target.write('\n')

def ensure_unicode(v):
    v = v.decode('utf-8', errors='ignore')
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

def get_title_author(text):
    author = "NULL"
    title = "NULL"
    text = text.splitlines()
    #for line in text, check if title or author stored there
    for i in range(80):
        try:
            if "Title: " in text[i]:
                title = text[i][7:]
            if "Author: " in text[i]:
                author = text[i][8:]
            #if they have both been found, do not waste extra time iterating 
            if title != "NULL" and author != "NULL":
                title_author_tuple = (title, author)
                return title_author_tuple
        except:
            pass
    title_author_tuple = (title, author)
    return title_author_tuple

def get_sentiment(temp):
    temp = temp.replace('\n', '')
    temp = temp.replace('\r', '')
    content = decode_file(temp)
    content = tokenize.sent_tokenize(content)
    #get author and title now that content is split by sentence 
    sid = SentimentIntensityAnalyzer()
    booksent = []
    for sentence in content:
        ss = sid.polarity_scores(sentence)
        ssarray = [ss['neg'],ss['neu'],ss['pos'], ss['compound']]
        booksent.append(ssarray)
    valuearray = np.array(booksent)
    # mean negative, neutral, positive, compound score for all lines in book
    values = np.mean(valuearray, axis=0)
    return values

def preprocessing():
    '''
    read file as a list of words
    set lowercase, stem, remove stopwords
    get punctuation string for later feature extraction
    save local wordcount dict
    save global word dict after finished looping through docs
    '''
    counter = 0
    for book in os.listdir("/Users/jamesledoux/Documents/James"):
        if not book.startswith('.'):    #pass hidden files such as .DS_STORE
            book = str(book)
            with open("/Users/jamesledoux/Documents/James/" + book, 'rb') as f:
                content = f.read().rstrip('\n')
            target.write(book + "|")
            punctAndWordsInSentence(content)
            sentiment_values = get_sentiment(content)
            neg = sentiment_values[0]
            neu = sentiment_values[1]
            pos = sentiment_values[2]
            compound = sentiment_values[3]
            target.write(str(neg) + "|" + str(neu) + "|" + str(pos) + "|" + str(compound) + "|" + str(counter) + "|")
            title_author_tuple = get_title_author(content)
            target.write(str(title_author_tuple[0]) + "|" + str(title_author_tuple[1]) + "|")
            content = content.translate(table, string.punctuation)
            content = ensure_unicode(content)
            content = content.decode("utf-8")
            content = content.split()
            target.write('\n')
            f.close()
            counter += 1
            if counter%20 == 0:
                print "book " + str(counter) + " done: " + book

preprocessing()
print datetime.now() - startTime

