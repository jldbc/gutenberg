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

#check avg sent size
target.write("book_name | total_words | avg_sentence_size | ! | /n | # | '' | % | $ | & | ')' | ( | + | * | - | , | / | . | ; | : | = | < | ? | > | @ | [ | ] | \ | _ | ^ | ` | { | } | '|' | ~ ")
target.write('\n')

def ensure_unicode(v):
    #if isinstance(v, str):
    v = v.decode('utf-8')
    return unicode(v)

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
        if not book.startswith('.'):    #pass hidden files such as .DS_STORE
            counter += 1
            book = str(book)
            with open("/Users/jamesledoux/Documents/txt_small/" + book, 'rb') as f:
                content = f.read().rstrip('\n')
            target.write(book + "|")
            punctAndWordsInSentence(content)
            content = content.translate(table, string.punctuation)
            content = ensure_unicode(content)
            content = content.decode("utf-8")
            content = content.split()
            target.write('\n')
            f.close()
            print "book " + str(counter) + " done: " + book
preprocessing()
