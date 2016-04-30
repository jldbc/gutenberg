from pyspark import SparkContext
from pyspark.mllib.feature import HashingTF
from pyspark.mllib.feature import IDF
import sys
import re


if __name__== "__main__":
    sc = SparkContext()
    docsDir = sys.argv[1]
    outputDir = sys.argv[2]
    #documents = sc.wholeTextFiles(docsDir).values().map(lambda doc: re.split('\W+', doc))
    documents = sc.wholeTextFiles(docsDir).values().map(lambda doc: re.split('\W+', doc))
    hashingTF = HashingTF()
    tf = hashingTF.transform(documents)
    tf.cache()
    idf = IDF().fit(tf)
    tfidf = idf.transform(tf)
    tfidf.saveAsTextFile(outputDir)
