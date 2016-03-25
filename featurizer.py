from __future__ import division
import csv
import os

"""
get punctuation dictionary here
later, use this + wordcount to get words per punct
also later, nwords / nperiods = avg sentence length (sentence complexity)
"""

#create a standardized list of punctuation marks
#will be easier later if we standardize the vector of these features now
punct_list = ['!', '/n', '#', '"', '%', '$', '&', ')', '(', '+', '*', '-', ',', '/', '.', ';', ':', '=', '<', '?', '>', '@', '[', ']', '\\', '_', '^', '`', '{', '}', '|', '~']

for book in os.listdir("/Users/jamesledoux/Documents/Big Data/gutenberg/punctuation/"):

    with open("/Users/jamesledoux/Documents/Big Data/gutenberg/punctuation/" + book, 'rb') as f:
        content = f.read()

    #first get punctuation dict of total occurences
    punctuation_dict = {}
    punct_count = 0
    for i in content:
        if i in punctuation_dict:
            punctuation_dict[i] = punctuation_dict[i] + 1
        else:
            punctuation_dict[i] = 1
        punct_count += 1

    #then relativize these offurences (mark occurences / total punct marks used)
    for item in punctuation_dict:
        punctuation_dict[item] = punctuation_dict[item]/punct_count

    #now write these in the order of the punct list
    writer = csv.writer(open("punct_dicts/" + book[:-4] + '.csv', 'w'))
    for i in range(len(punct_list)):
        try:
            writer.writerow([punct_list[i], punctuation_dict[punct_list[i]]])
            print punctuation_dict[punct_list[i]]
        except:
            writer.writerow([punct_list[i], 0])
