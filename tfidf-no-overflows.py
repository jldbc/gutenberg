from pyspark import SparkConf, SparkContext
from pyspark.mllib.feature import HashingTF
from pyspark.mllib.feature import IDF
from pyspark.mllib.clustering import KMeans, KMeansModel
from pyspark.mllib.linalg import SparseVector
from os.path import join
from pyspark.mllib.util import MLUtils
from pyspark.mllib.feature import StandardScaler
from pyspark.mllib.linalg import Vectors
import pandas as pd
from numpy import array
from collections import Counter
from pyspark.mllib.util import MLUtils
import sys
import re


if __name__== "__main__":
    sc = SparkContext()
    docsDir = sys.argv[1]
    outputDir = sys.argv[2]
    documents = sc.wholeTextFiles(docsDir).values().map(lambda doc: re.split('\W+', doc))
    hashingTF = HashingTF()
    tf = hashingTF.transform(documents)
    tf.cache()
    idf = IDF(minDocFreq=3).fit(tf)
    tfidf = idf.transform(tf)

    #temp = tfidf.collect()[0]
    #standardizer = StandardScaler(True, True)
    #model = standardizer.fit(temp)
    #result = model.transform(tfidf.collect())
    #tfidf.saveAsTextFile(outputDir)
    print "********* tfidf done ***********"
    clusters = KMeans.train(tfidf, 10, maxIterations=100)
    #print "model trained"
    #clusters.save(sc, "KMeansModel")


    membership2 = []
    sparse_data = tfidf.collect()
    words_map = {}
    for i in range(len(sparse_data)):
        clusterid = clusters.predict(sparse_data[i])
        membership2.append(clusterid)
        print 'cluster id: %d' % clusterid

    print membership2
    #clusters.save(sc, "KMeansModel")





#