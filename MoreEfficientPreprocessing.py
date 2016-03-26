from __future__ import division
from nltk.stem.snowball import *
import string
import os
import pickle
import csv
import sys

#need this or else it throws encoding/decoding errors
reload(sys)
sys.setdefaultencoding('utf8')
punct = set(['!', '/n', '#', '"', '%', '$', '&', ')', '(', '+', '*', '-', ',', '/', '.', ';', ':', '=', '<', '?', '>', '@', '[', ']', '\\', '_', '^', '`', '{', '}', '|', '~'])
table = string.maketrans("","")
target = open("output.txt", 'w')

def ensure_unicode(v):
    #if isinstance(v, str):
    v = v.decode('utf-8')
    return unicode(v)

def punctAndWordsInSentence(listOCharacters):
    punctuation_dict = {}
    sentenceCounter = 0;
    wordCounter = 0
    periodCounter = 0;
    avgSentenceSize = 0;
    totalWords = 0;
    punctCounter = 0;
    for i in listOCharacters:
        if i == ' ':
            wordCounter = wordCounter + 1
        if i == '.':
            periodCounter = periodCounter + 1
            totalWords = totalWords + wordCounter
            avgSentenceSize = (totalWords + wordCounter) / periodCounter
            wordCounter = 0
        if i in punct:
            punctCounter = punctCounter + 1
            if i in punctuation_dict:
                punctuation_dict[i] = punctuation_dict[i]+1
            else:
                punctuation_dict[i] = 1
    target.write(str(avgSentenceSize) + ", ")
    s = ""
    for i in punct:
        if i in punctuation_dict:
            s = s + str(i) + "|" + str(punctuation_dict[i] / punctCounter) + " "
    target.write(s + ", ")

        
##    punct_string = ""
##    punct_string = punct_string.join(x for x in listOCharacters if x in punct)
##    return punct_string
    
def preprocessing():
    '''
    read file as a list of words
    set lowercase, stem, remove stopwords
    get punctuation string for later feature extraction
    save local wordcount dict
    save global word dict after finished looping through docs
    '''
    counter = 0
    for book in os.listdir("/Users/jamesledoux/Documents/txt_small"):
        counter += 1
        book = str(book)
        with open("/Users/jamesledoux/Documents/txt_small/" + book, 'rb') as f:
            content = f.read().rstrip('\n')
        target.write(book + ", ")
        punctAndWordsInSentence(content)
        content = content.translate(table, string.punctuation)
        content = ensure_unicode(content)
        content = content.decode("utf-8")
        content = content.split()
        target.write( str( len(content)))
        target.write('\n')
        f.close()
        print "book " + str(counter) + " done: " + book
preprocessing()
## Output is something like this:
## Name_of_Book, average_sentence_size, punct|punct_freq, number_of_words

        
        
        
    
