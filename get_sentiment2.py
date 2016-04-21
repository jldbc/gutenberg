from nltk.classify import NaiveBayesClassifier
from nltk.corpus import subjectivity
from nltk.sentiment import SentimentAnalyzer
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
from nltk import tokenize
import numpy as np
import pandas as pd
import os


"""
some of the nltk dependencies are problematic here
make sure whatever we run this on has nltk/. . ./ . . ./vader,
vader_lexicon.txt
and other things installed or else this will just throw errors

-- maybe create a dependencies folder for the repo, and import vader + other sentiment
   tools from that folder? nltk asks you to download additional materials, so this might
   be a less confusing experience

TODO:
- experiment with training set sizes, see if this improves model performance
"""

def decode_file(text):
    return text.decode('utf-8')

#train the model
n_instances = 100
subj_docs = [(sent, 'subj') for sent in subjectivity.sents(categories='subj')[:n_instances]]
obj_docs = [(sent, 'obj') for sent in subjectivity.sents(categories='obj')[:n_instances]]
len(subj_docs), len(obj_docs)

subj_docs[0]
train_subj_docs = subj_docs[:80]
test_subj_docs = subj_docs[80:100]
train_obj_docs = obj_docs[:80]
test_obj_docs = obj_docs[80:100]

training_docs = train_subj_docs+train_obj_docs
testing_docs = test_subj_docs+test_obj_docs
sentim_analyzer = SentimentAnalyzer()
all_words_neg = sentim_analyzer.all_words([mark_negation(doc) for doc in training_docs])


unigram_feats = sentim_analyzer.unigram_word_feats(all_words_neg, min_freq=4)
sentim_analyzer.add_feat_extractor(extract_unigram_feats, unigrams=unigram_feats)

training_set = sentim_analyzer.apply_features(training_docs)
test_set = sentim_analyzer.apply_features(testing_docs)

trainer = NaiveBayesClassifier.train
classifier = sentim_analyzer.train(trainer, training_set)

print "model trained. . ."

#read previous output file
path = "/Users/jamesledoux/Documents/BigData/gutenberg/output.txt"
data = pd.read_csv(path, sep="|")
data=data.rename(columns = {'book_name ':'book_name'})
data['sentiment_negative'] = 999999
data['sentiment_neutral'] = -999999
data['sentiment_positive'] = -999999
data['sentiment_compound'] = 0
counter = 0
for book in os.listdir("/Users/jamesledoux/Documents/txt_small"):
    if not book.startswith('.'):
        #read file, remove \r and \n's, split by sentence
        with open("/Users/jamesledoux/Documents/txt_small/" + book, 'rb') as f:
            temp = f.read()
        temp = temp.replace('\n', '')
        temp = temp.replace('\r', '')
        #avoid encoding errors before splitting by sentence
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
        print " "
        print "Sentiment scores for book " + str(counter) + ": " + str(book)
        print "neg: " + str(values[0]) + "  neu: " + str(values[1]) + "  pos: " + str(values[2]) + "  compound: " + str(values[3])
        data.loc[data.book_name == book, 'sentiment_negative'] = values[0]
        data.loc[data.book_name == book, 'sentiment_neutral'] = values[1]
        data.loc[data.book_name == book, 'sentiment_positive'] = values[2]
        data.loc[data.book_name == book, 'sentiment_compound'] = values[3]
        data.loc[data.book_name == book, 'ID'] = counter
        counter += 1

        #with open("sentiments/" + book[:-4] + ".csv", 'w') as f:
        #    f.write(str(values[0]) + ", " + str(values[1]) + ", " + str(values[2]) + ", " + str(values[3]))
        #f.close()

data.to_csv('/Users/jamesledoux/Documents/BigData/gutenberg/output.csv')
