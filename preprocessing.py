from nltk.stem.snowball import *
import string
import os
import pickle
import csv
import sys

#need this or else it throws encoding/decoding errors
reload(sys)
sys.setdefaultencoding('utf8')

table = string.maketrans("","")
stopwords = [line.rstrip('\n') for line in open('princetonStopWords.txt')]

globaldict = {}
punct = set(['!', '/n', '#', '"', '%', '$', '&', ')', '(', '+', '*', '-', ',', '/', '.', ';', ':', '=', '<', '?', '>', '@', '[', ']', '\\', '_', '^', '`', '{', '}', '|', '~'])


for i in range(len(stopwords)):
    stopwords[i] = stopwords[i].translate(table, string.punctuation)

def ensure_unicode(v):
    #if isinstance(v, str):
    v = v.decode('utf-8')
    return unicode(v)

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
        book = str(book)
        counter += 1
        punct_string = ""
        with open("/Users/jamesledoux/Documents/txt_small/" + book, 'rb') as f:
            content = f.read().rstrip('\n')
        punct_string = punct_string.join(x for x in content if x in punct)
        content = content.translate(table, string.punctuation)
        content = ensure_unicode(content)
        content = content.decode("utf-8")
        content = content.split()
        #set lowercase
        for i in range(len(content)):
            content[i] = content[i].lower()
        content2 = []
        #stopwords
        for i in range(len(content)):
            if content[i] not in stopwords:
                content2.append(content[i])
        #stemming
        stemmer = SnowballStemmer("english")
        for i in range(len(content2)):
            content2[i] = stemmer.stem(content2[i])
        #populate local dict of wordcounts
        #if word not in global dict yet, add it in & set to 0
        localdict = {}
        for i in content2:
            if i in localdict:
                localdict[i] += 1
            else:
                localdict[i] = 1
            if i not in globaldict:
                globaldict[i] = 0
        writer = csv.writer(open(book[:-4] + '.csv', 'wb'))
        for key, value in localdict.items():
           writer.writerow([key, value])

        with open("punctuation/" + book, 'w') as f:
            f.write(punct_string)
        f.close()

        print "book " + str(counter) + " done: " + book


preprocessing()
writer2 = csv.writer(open('global_word_dict.csv', 'wb'))
for key, value in globaldict.items():
   writer2.writerow([key, value])
