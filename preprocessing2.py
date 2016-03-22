from stemming.porter2 import stem
import string
import os
import pickle
import csv
import sys
import string
import time
import glob
import fnmatch

reload(sys)
sys.setdefaultencoding('utf8')

table = string.maketrans("","")

stop_words = [line.rstrip('\n') for line in open('princetonStopWords.txt')]
for i in range(len(stop_words)):
    stop_words[i] = stop_words[i].translate(table, string.punctuation)

globaldict = {}
files = ["Abraham Lincoln___Lincoln's Gettysburg Address", "Beatrix Potter___The Story of Miss Moppet", "Bret Harte___Excelsior", "Beatrix Potter___Cecily Parsley's Nursery Rhymes", "Abraham Lincoln___The Emancipation Proclamation"]
punct = set(['!', '/n', '#', '"', '%', '$', '&', ')', '(', '+', '*', '-', ',', '/', '.', ';', ':', '=', '<', '?', '>', '@', '[', ']', '\\', '_', '^', '`', '{', '}', '|', '~'])
counter = 0

def ensure_unicode(v):
    #if isinstance(v, str):
    v = v.decode('utf-8')
    return unicode(v)
    
def print_global_dict():
    writer2 = csv.writer(open('global_word_dict.csv', 'wb'))
    for key, value in globaldict.items():
       writer2.writerow([key, value])

def loopProcess():
    # for i in range(len(files)):
    #     preprocessing(files[i])
    # for book in glob.iglob("txt/*.txt"):
    #     book = str(book)
    #     preprocessing(book)
    matches = []
    count = 0
    for root, dirnames, filenames in os.walk('txt'):
        for filename in fnmatch.filter(filenames, '*.txt'):
            #matches.append(filename)
            if (count < 6):
                preprocessing(filename[:-4])
                count += 1
    #print matches

def preprocessing(fileName):
    #counter += 1
    """
    set to lowercase
    remove stopwords:   remove as you add to list. will want them in the original data for stylistic stuff so don't remove from that
    stem the words


    creates a local hash table (k: word, v: occurences) for each document. create global dict as you go,
    with all words set to zero occurences.

    next pass:
    for each file,  for word in global dict,  add n of local occurences to vector. can now
    cluster on this sparse vector.
    """

    """
    globaldict = {}
    for file in all files:
        localdict = {}
        for word in file
            if word in localdict exists
                localdict[word] += 1
            else:
                localdict[word] = 1
            if word in globaldict:
                pass
            else:
                globadict[word] = 0
    """

    start = time.clock()
    #remove ' characters from stopwords list.. bc they will be removed from the text itself also and they need to match


    #iterate through all files  : : : : :

    #read file as a list of words
    #also get rid of punctuation so it can be stemmed / put into dict
    #but also keep puncutation marks for later features
    #punct = set(string.punctuation)
    punct_string = ""
#######################################################################################
    # Use this for Single file reads 
    with open("txt/" + fileName + ".txt", 'rb') as f:
        content = f.read().rstrip('\n')
#######################################################################################
    # Use this for folder reads
    # with open(fileName, 'rb') as f:
    #     content = f.read().rstrip('\n')
#######################################################################################
    punct_string = punct_string.join(x for x in content if x in punct)
    content = content.translate(table, string.punctuation)
    content = ensure_unicode(content)
    content = content.decode("utf-8")
    content = content.split()

    #set lowercase
    for i in range(len(content)):
        content[i] = content[i].lower()

    #stopwords
    content2 = []
    for i in range(len(content)):
        if content[i] not in stop_words:
            content2.append(content[i])

    #stemming
    #stemmer = SnowballStemmer("english")

    for i in range(len(content2)):
        content2[i] = stem(content2[i])

    #populate local dict of wordcounts
    #if word not yet in global dict, add that key to global dict
    localdict = {}
    for i in content2:
        if i in localdict:
            localdict[i] += 1
        else:
            localdict[i] = 1
        if i not in globaldict:
            globaldict[i] = 0
    writer = csv.writer(open("local_dictionaries/" + fileName + '.csv', 'wb'))
    for key, value in localdict.items():
       writer.writerow([key, value])

    with open("punctuation/" + fileName, 'w') as f:
        f.write(punct_string)
    f.close()

    end = time.clock()
    print (end - start)
    #print "book " + str(counter) + " done: " + fileName[4:]
    print "book done: " + fileName + " "
    
    #