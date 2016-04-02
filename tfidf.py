
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
		self.stopWords = set(['the','and','a','am','an','are',"aren't",'but',\
							  'on','had','have','at','for','that','is','he','i',\
							  'she','they','their','we','were',"weren't",'so',
							  'to','too','of','very','was','not','it','its','com',\
							  "it's",'all','as','be','by','cannot',"can't",'or',\
							  'this','those','what','who','which','why','me','our',\
							  'you','yourself','yours','mine','ours','theirs','hers',\
							  'his','her','these',"i've","i'm","we're","i'll","we'll",\
							  "we've","he'd","she'd","he's","she's","they're",'when',\
							  'them','him','us','your','when','where'])

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
			writer.writerow(['docID','word','score'])
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
		tfidf = wcRDD.join(wfRDD).map(lambda (w,((d,a,b),c)): ((d,-a/b * np.log(D.value/c),w),1))\
					 .sortByKey(True).map(lambda ((d,z,w),a): (d,w,-z))
		self.writeToCSVFile(tfidf.collect())

# - - - - - - - - - - - - - - - - - - - - SCRIPT STARTS HERE - - - - - - - - - - - - - - - - - - - - #
tfRes = TFIDF(sys.argv[1],sys.argv[2])
tfRes.run()
#/Users/jamesledoux/spark-1.6.1/bin/spark-submit /Users/jamesledoux/Documents/BigData/gutenberg/tfidf.py "/Users/jamesledoux/Documents/txt_small2/" "/Users/jamesledoux/Documents/BigData/gutenberg/TFIDF Output"
