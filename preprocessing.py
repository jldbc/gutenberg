from __future__ import division
from nltk.stem.snowball import *
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from nltk.sentiment.util import *
from nltk import tokenize
from datetime import datetime
import nltk
import numpy as np
import string
import csv
import sys
import os

"""
TODO: STORE SENTIMENT INFO IN A WAY THAT ALLOWS US TO CREATE RUNNING SENTIMENT GRAPHS

- Cut text into 20 or so roughly equal sized chunks of sentences
- Store mean positive and negative sentiment values for each segment as a feature 
- Create graphs of sentiment movement for data viz (upper bound == max value observed, lower bound == 0)

"""
startTime = datetime.now()
#need this or else it throws encoding/decoding errors
reload(sys)
sys.setdefaultencoding('utf8')
punct = set(['!', '#', '"', '%', '$', '&', '(', '+', '*', '-', ',', '/', '.', ';', ':', '=', '<', '?', '>', '@', '[', ']', '_', '^', '`', '{', '~'])
table = string.maketrans("","")
target = open("output_POS.txt", 'w')

#check avg sent size
target.write("book_name|total_words|avg_sentence_size|!|#|''|%|$|&|(|+|*|-|,|/|.|;|:|=|<|?|>|@|[|]|_|^|`|{|~|neg|neu|pos|compound|ID|Title|Author|CC|CD|DT|EX|FW|IN|JJ|JJR|JJS|LS|MD|NN|NNP|NNPS|NNS|PDT|PRP|PRP$|RB|RBR|RBS|RP|VB|VBD|VBG|VBP|VBN|WDT|VBZ|WRB|WP$|WP|")
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
    #sentence count
    for i in range(len(listOfCharacters)):
        if i != 0:
            #if lettter followed by space or punct, then word count +=1
            if (listOfCharacters[i] == " " or str(listOfCharacters[i]) in punct) and str(listOfCharacters[i-1]) in (string.ascii_lowercase + string.ascii_uppercase):
                totalWords = totalWords + 1
            #count periods as well
            if listOfCharacters[i] == ".":
                periodCounter = periodCounter + 1
            if listOfCharacters[i] in punct:
                punctCounter = punctCounter + 1
                if listOfCharacters[i] in punctuation_dict:
                    punctuation_dict[listOfCharacters[i]] = punctuation_dict[listOfCharacters[i]] + 1
                else:
                    punctuation_dict[listOfCharacters[i]] = 1



    avgSentenceSize = (totalWords/periodCounter)
    #put together output, bar delimited
    target.write(str(totalWords) + "|")
    target.write(str(avgSentenceSize) + "|")
    
    for i in punct:
        s = ""
        if i in punctuation_dict:
            s = s + str(punctuation_dict[i] / punctCounter) + "|"    #pct of punct that is [x]
        else:
            s = s + str(0) + "|"                                     #0 if unused
        target.write(s)


def pos_tagging(content):
    parts = ["CC", "CD", "DT", "EX", "FW", "IN", "JJ", "JJR", "JJS", "LS", "MD", "NN", "NNP", "NNPS", "NNS", "PDT", "PRP", "PRP$", "RB", "RBR", "RBS", "RP", "VB", "VBD", "VBG",  "VBP", "VBN", "WDT", "VBZ", "WRB", "WP$", "WP" ]
    content = ensure_unicode(content)   #see if this fixes the error
    text = nltk.word_tokenize(content)  #need to tokenize first
    results = nltk.pos_tag(text)
    #dict of {POS: count}
    results_dict = {}
    counter = 0
    for tag in results:
        token = tag[0]
        pos = tag[1]
        counter += 1
        if pos in results_dict:
            results_dict[pos] += 1
        else:
            results_dict[pos] = 1
    #write to file
    for i in parts:
        s = ""
        if i in results_dict:
            s = s + str(results_dict[i]/float(counter)) + "|"    #pct of POS that are [x]
        else:
            s = s + str(0) + "|"                                 #0 if unused
        target.write(s)

def decode_file(text):
    return text.decode('utf-8', errors='replace')

def get_title_author(text):
    author = "NULL"
    title = "NULL"
    text = text.splitlines()
    #for line in text, check if title or author stored there
    for i in range(80):
        #error handling since some texts are <80 lines
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
    for book in os.listdir("/Users/jamesledoux/Documents/Drew"):
        if not book.startswith('.'):    #pass hidden files such as .DS_STORE
            book = str(book)
            with open("/Users/jamesledoux/Documents/Drew/" + book, 'rb') as f:
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
            pos_tagging(content)
            target.write('\n')
            f.close()
            counter += 1
            if counter%20 == 0:
                print "book " + str(counter) + " done: " + book

preprocessing()
print datetime.now() - startTime

"""
POS Tagging Key: 

$: dollar
    $ -$ --$ A$ C$ HK$ M$ NZ$ S$ U.S.$ US$
'': closing quotation mark
    ' ''
(: opening parenthesis
    ( [ {
): closing parenthesis
    ) ] }
,: comma
    ,
--: dash
    --
.: sentence terminator
    . ! ?
:: colon or ellipsis
    : ; ...
CC: conjunction, coordinating
    & 'n and both but either et for less minus neither nor or plus so
    therefore times v. versus vs. whether yet
CD: numeral, cardinal
    mid-1890 nine-thirty forty-two one-tenth ten million 0.5 one forty-
    seven 1987 twenty '79 zero two 78-degrees eighty-four IX '60s .025
    fifteen 271,124 dozen quintillion DM2,000 ...
DT: determiner
    all an another any both del each either every half la many much nary
    neither no some such that the them these this those
EX: existential there
    there
FW: foreign word
    gemeinschaft hund ich jeux habeas Haementeria Herr K'ang-si vous
    lutihaw alai je jour objets salutaris fille quibusdam pas trop Monte
    terram fiche oui corporis ...
IN: preposition or conjunction, subordinating
    astride among uppon whether out inside pro despite on by throughout
    below within for towards near behind atop around if like until below
    next into if beside ...
JJ: adjective or numeral, ordinal
    third ill-mannered pre-war regrettable oiled calamitous first separable
    ectoplasmic battery-powered participatory fourth still-to-be-named
    multilingual multi-disciplinary ...
JJR: adjective, comparative
    bleaker braver breezier briefer brighter brisker broader bumper busier
    calmer cheaper choosier cleaner clearer closer colder commoner costlier
    cozier creamier crunchier cuter ...
JJS: adjective, superlative
    calmest cheapest choicest classiest cleanest clearest closest commonest
    corniest costliest crassest creepiest crudest cutest darkest deadliest
    dearest deepest densest dinkiest ...
LS: list item marker
    A A. B B. C C. D E F First G H I J K One SP-44001 SP-44002 SP-44005
    SP-44007 Second Third Three Two * a b c d first five four one six three
    two
MD: modal auxiliary
    can cannot could couldn't dare may might must need ought shall should
    shouldn't will would
NN: noun, common, singular or mass
    common-carrier cabbage knuckle-duster Casino afghan shed thermostat
    investment slide humour falloff slick wind hyena override subhumanity
    machinist ...
NNP: noun, proper, singular
    Motown Venneboerger Czestochwa Ranzer Conchita Trumplane Christos
    Oceanside Escobar Kreisler Sawyer Cougar Yvette Ervin ODI Darryl CTCA
    Shannon A.K.C. Meltex Liverpool ...
NNPS: noun, proper, plural
    Americans Americas Amharas Amityvilles Amusements Anarcho-Syndicalists
    Andalusians Andes Andruses Angels Animals Anthony Antilles Antiques
    Apache Apaches Apocrypha ...
NNS: noun, common, plural
    undergraduates scotches bric-a-brac products bodyguards facets coasts
    divestitures storehouses designs clubs fragrances averages
    subjectivists apprehensions muses factory-jobs ...
PDT: pre-determiner
    all both half many quite such sure this
POS: genitive marker
    ' 's
PRP: pronoun, personal
    hers herself him himself hisself it itself me myself one oneself ours
    ourselves ownself self she thee theirs them themselves they thou thy us
PRP$: pronoun, possessive
    her his mine my our ours their thy your
RB: adverb
    occasionally unabatingly maddeningly adventurously professedly
    stirringly prominently technologically magisterially predominately
    swiftly fiscally pitilessly ...
RBR: adverb, comparative
    further gloomier grander graver greater grimmer harder harsher
    healthier heavier higher however larger later leaner lengthier less-
    perfectly lesser lonelier longer louder lower more ...
RBS: adverb, superlative
    best biggest bluntest earliest farthest first furthest hardest
    heartiest highest largest least less most nearest second tightest worst
RP: particle
    aboard about across along apart around aside at away back before behind
    by crop down ever fast for forth from go high i.e. in into just later
    low more off on open out over per pie raising start teeth that through
    under unto up up-pp upon whole with you
SYM: symbol
    % & ' '' ''. ) ). * + ,. < = > @ A[fj] U.S U.S.S.R * ** ***
TO: "to" as preposition or infinitive marker
    to
UH: interjection
    Goodbye Goody Gosh Wow Jeepers Jee-sus Hubba Hey Kee-reist Oops amen
    huh howdy uh dammit whammo shucks heck anyways whodunnit honey golly
    man baby diddle hush sonuvabitch ...
VB: verb, base form
    ask assemble assess assign assume atone attention avoid bake balkanize
    bank begin behold believe bend benefit bevel beware bless boil bomb
    boost brace break bring broil brush build ...
VBD: verb, past tense
    dipped pleaded swiped regummed soaked tidied convened halted registered
    cushioned exacted snubbed strode aimed adopted belied figgered
    speculated wore appreciated contemplated ...
VBG: verb, present participle or gerund
    telegraphing stirring focusing angering judging stalling lactating
    hankerin' alleging veering capping approaching traveling besieging
    encrypting interrupting erasing wincing ...
VBN: verb, past participle
    multihulled dilapidated aerosolized chaired languished panelized used
    experimented flourished imitated reunifed factored condensed sheared
    unsettled primed dubbed desired ...
VBP: verb, present tense, not 3rd person singular
    predominate wrap resort sue twist spill cure lengthen brush terminate
    appear tend stray glisten obtain comprise detest tease attract
    emphasize mold postpone sever return wag ...
VBZ: verb, present tense, 3rd person singular
    bases reconstructs marks mixes displeases seals carps weaves snatches
    slumps stretches authorizes smolders pictures emerges stockpiles
    seduces fizzes uses bolsters slaps speaks pleads ...
WDT: WH-determiner
    that what whatever which whichever
WP: WH-pronoun
    that what whatever whatsoever which who whom whosoever
WP$: WH-pronoun, possessive
    whose
WRB: Wh-adverb
    how however whence whenever where whereby whereever wherein whereof why
``: opening quotation mark
    ` ``

"""

#
