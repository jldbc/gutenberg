
# Apache Spark MapReduce Implementation of TF-IDF in Python 2.7.10.
# Copyright (c) 2016 Pragaash Ponnusamy.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# - - - - - - - - - IMPORT - - - - - - - - -#
from __future__ import division
from glob import glob
from pyspark import SparkContext, SparkConf
import operator,re,csv,sys
import numpy as np
from pyspark.mllib.feature import HashingTF
from pyspark.mllib.feature import IDF

#pyspark command line: /Users/jamesledoux/spark-1.6.1/bin/pyspark
# - - - - - - - - - - - - - - - - - - - - - #

class TextFilter():

	def __init__(self):
		self.stopWords = set(["a's", 'able', 'about', 'above', 'according', 'accordingly', 'across', 'actually',\
							 'after', 'afterwards', 'again', 'against', "ain't", 'all', 'allow', 'allows', 'almost',\
							 'alone', 'along', 'already', 'also', 'although', 'always', 'am', 'among', 'amongst', 'an',\
							 'and', 'another', 'any', 'anybody', 'anyhow', 'anyone', 'anything', 'anyway', 'anyways', 'anywhere',\
							 'apart', 'appear', 'appreciate', 'appropriate', 'are', "aren't", 'around', 'as', 'aside', 'ask',\
							 'asking', 'associated', 'at', 'available', 'away', 'awfully', 'be', 'became', 'because', 'become',\
							 'becomes', 'becoming', 'been', 'before', 'beforehand', 'behind', 'being', 'believe', 'below', 'beside',\
							 'besides', 'best', 'better', 'between', 'beyond', 'both', 'brief', 'but', 'by', "c'mon", "c's", 'came',\
							 'can', "can't", 'cannot', 'cant', 'cause', 'causes', 'certain', 'certainly', 'changes', 'clearly', 'co',\
							 'com', 'come', 'comes', 'concerning', 'consequently', 'consider', 'considering', 'contain', 'containing',
							 'contains', 'corresponding', 'could', "couldn't", 'course', 'currently', 'definitely', 'described', 'despite',
							 'did', "didn't", 'different', 'do', 'does', "doesn't", 'doing', "don't", 'done', 'down', 'downwards',
							 'during', 'each', 'edu', 'eg', 'eight', 'either', 'else', 'elsewhere', 'enough', 'entirely', 'especially',
							 'et', 'etc', 'even', 'ever', 'every', 'everybody', 'everyone', 'everything', 'everywhere', 'ex', 'exactly',
							 'example', 'except', 'far', 'few', 'fifth', 'first', 'five', 'followed', 'following', 'follows', 'for',
							 'former', 'formerly', 'forth', 'four', 'from', 'further', 'furthermore', 'get', 'gets', 'getting',
							 'given', 'gives', 'go', 'goes', 'going', 'gone', 'got', 'gotten', 'greetings', 'had', "hadn't",
							 'happens', 'hardly', 'has', "hasn't", 'have', "haven't", 'having', 'he', "he's", 'hello', 'help',
							 'hence', 'her', 'here', "here's", 'hereafter', 'hereby', 'herein', 'hereupon', 'hers', 'herself',
							 'hi', 'him', 'himself', 'his', 'hither', 'hopefully', 'how', 'howbeit', 'however', "i'd", "i'll",
							 "i'm", "i've", 'ie', 'if', 'ignored', 'immediate', 'in', 'inasmuch', 'inc', 'indeed', 'indicate',
							 'indicated', 'indicates', 'inner', 'insofar', 'instead', 'into', 'inward', 'is', "isn't", 'it',
							 "it'd", "it'll", "it's", 'its', 'itself', 'just', 'keep', 'keeps', 'kept', 'know', 'knows', 'known',
							 'last', 'lately', 'later', 'latter', 'latterly', 'least', 'less', 'lest', 'let', "let's", 'like',
							 'liked', 'likely', 'little', 'look', 'looking', 'looks', 'ltd', 'mainly', 'many', 'may', 'maybe',
							 'me', 'mean', 'meanwhile', 'merely', 'might', 'more', 'moreover', 'most', 'mostly', 'much', 'must',
							 'my', 'myself', 'name', 'namely', 'nd', 'near', 'nearly', 'necessary', 'need', 'needs', 'neither',
							 'never', 'nevertheless', 'new', 'next', 'nine', 'no', 'nobody', 'non', 'none', 'noone', 'nor',
							 'normally', 'not', 'nothing', 'novel', 'now', 'nowhere', 'obviously', 'of', 'off', 'often',
							 'oh', 'ok', 'okay', 'old', 'on', 'once', 'one', 'ones', 'only', 'onto', 'or', 'other', 'others',
							 'otherwise', 'ought', 'our', 'ours', 'ourselves', 'out', 'outside', 'over', 'overall', 'own',
							 'particular', 'particularly', 'per', 'perhaps', 'placed', 'please', 'plus', 'possible', 'presumably',
							 'probably', 'provides', 'que', 'quite', 'qv', 'rather', 'rd', 're', 'really', 'reasonably',
							 'regarding', 'regardless', 'regards', 'relatively', 'respectively', 'right', 'said', 'same',
							 'saw', 'say', 'saying', 'says', 'second', 'secondly', 'see', 'seeing', 'seem', 'seemed',
							 'seeming', 'seems', 'seen', 'self', 'selves', 'sensible', 'sent', 'serious', 'seriously',
							 'seven', 'several', 'shall', 'she', 'should', "shouldn't", 'since', 'six', 'so', 'some',
							 'somebody', 'somehow', 'someone', 'something', 'sometime', 'sometimes', 'somewhat',
							 'somewhere', 'soon', 'sorry', 'specified', 'specify', 'specifying', 'still', 'sub',
							 'such', 'sup', 'sure', "t's", 'take', 'taken', 'tell', 'tends', 'th', 'than', 'thank',
							 'thanks', 'thanx', 'that', "that's", 'thats', 'the', 'their', 'theirs', 'them', 'themselves',
							 'then', 'thence', 'there', "there's", 'thereafter', 'thereby', 'therefore', 'therein',
							 'theres', 'thereupon', 'these', 'they', "they'd", "they'll", "they're", "they've", 'think',
							 'third', 'this', 'thorough', 'thoroughly', 'those', 'though', 'three', 'through',
							 'throughout', 'thru', 'thus', 'to', 'together', 'too', 'took', 'toward', 'towards',
							 'tried', 'tries', 'truly', 'try', 'trying', 'twice', 'two', 'un', 'under', 'unfortunately',
							 'unless', 'unlikely', 'until', 'unto', 'up', 'upon', 'us', 'use', 'used', 'useful',
							 'uses', 'using', 'usually', 'value', 'various', 'very', 'via', 'viz', 'vs', 'want',
							 'wants', 'was', "wasn't", 'way', 'we', "we'd", "we'll", "we're", "we've", 'welcome',
							 'well', 'went', 'were', "weren't", 'what', "what's", 'whatever', 'when', 'whence',
							 'whenever', 'where', "where's", 'whereafter', 'whereas', 'whereby', 'wherein',
							 'whereupon', 'wherever', 'whether', 'which', 'while', 'whither', 'who', "who's",
							 'whoever', 'whole', 'whom', 'whose', 'why', 'will', 'willing', 'wish', 'with',
							 'within', 'without', "won't", 'wonder', 'would', 'would', "wouldn't", 'yes',
							 'yet', 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself',
							 'yourselves', 'zero'])

	def filter(self,text):
		return filter(lambda word: word not in self.stopWords,\
					  re.findall('[\w+]{2,}',re.sub('[0-9]','',text.lower().strip())))

class TFIDF():

	def __init__(self,input_path,output_path):
		self.input = input_path
		self.output = output_path
		self.texts = glob(self.input + '/*.txt')
		self.conf = SparkConf().setAppName('tfidf')\
							   .setMaster('local')\
							   .set('spark.executor.memory','1g')
		self.sc = SparkContext(conf=self.conf)

	def writeToCSVFile(self,rdd):
		with open(self.output + '/tfidf-scores.csv','wb') as csvfile:
			writer = csv.writer(csvfile)
			#writer.writerow(['docID','word','score'])
			writer.writerows(rdd)


	def run(self):
		# Job 1: Word Frequency in Documents.
		tfilter = TextFilter().filter
		wcRDD = self.sc.emptyRDD()
		for dkey,textfile in enumerate(self.texts):
			tf = self.sc.textFile(textfile)\
					 .filter(lambda line: len(line.strip()) > 0)\
				     .flatMap(lambda line: tfilter(line))\
				     .map(lambda word: ((word,dkey),1))\
				     .reduceByKey(operator.add)
			N = tf.map(lambda ((w,d),y): y).sum()
			tf = tf.map(lambda ((w,d),y): ((w,d),(y,N)))
			wcRDD = self.sc.union([wcRDD,tf])

		# Job 2: Word Frequency in Corpus & Calculate TF-IDF.
		D = self.sc.broadcast(len(self.texts))
		wcRDD = wcRDD.map(lambda ((w,d),(a,b)): (w,(d,a,b)))
		wfRDD = wcRDD.map(lambda (w,(d,a,b)): (w,1)).reduceByKey(operator.add)
		
		words_list = wfRDD.collect()
		unzip1, unzip2 = zip(*words_list)
		with open("words_to_id.txt", "w") as text_file:
			for word in unzip1:
				text_file.write(str(word.decode('utf-8')) + '\n')
		#print(wfRDD.collect())

		tfidf = wcRDD.join(wfRDD).map(lambda (w,((d,a,b),c)): ((d,-a/b * np.log(D.value/c),w),1))\
					 .sortByKey(True).map(lambda ((d,z,w),a): (d,w,-z))
		self.writeToCSVFile(tfidf.collect())

# - - - - - - - - - - - - - - - - - - - - SCRIPT STARTS HERE - - - - - - - - - - - - - - - - - - - - #
tfRes = TFIDF(sys.argv[1],sys.argv[2])
tfRes.run()
#/Users/jamesledoux/spark-1.6.1/bin/spark-submit /Users/jamesledoux/Documents/BigData/gutenberg/tfidf.py "/Users/jamesledoux/Documents/txt_small2/" "/Users/jamesledoux/Documents/BigData/gutenberg/TFIDF Output"
