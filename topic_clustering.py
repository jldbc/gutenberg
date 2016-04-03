from pyspark.mllib.clustering import KMeans, KMeansModel
from pyspark.mllib.linalg import SparseVector
from pyspark import SparkConf, SparkContext
from os.path import join
import sys


"""
kmeans(data, k, ...)

rows
uid, movid, rating, timestamp

make a matrix:    cols words, rows Books


/Users/jamesledoux/spark-1.6.1/bin/spark-submit  /Users/jamesledoux/Documents/BigData/gutenberg/topic_clustering.py  /Users/jamesledoux/Documents/BigData/gutenberg/
/Users/jamesledoux/spark-1.6.1/bin/pyspark

"""
if(len(sys.argv) != 2):
    print "usage: /sparkPath/bin/spark-submit  name.py  movieDirectory"

conf = SparkConf().setAppName("KMeans TF-IDF").set("spark.executor.memory", "15g")
#sc = SparkContext(conf)
HomeDir = sys.argv[1]   # passed as argument
#HomeDir = "/Users/jamesledoux/Documents/Big\ Data/movielens/medium/"
#HomeDir = "/Users/jamesledoux/Documents/BigData/gutenberg/"
sc = SparkContext()
#SparkContext.setSystemProperty('spark.executor.memory', '4g')


def parseWords(line):
    #uid::wordID::rating::timestamp
    parts = line.strip().split(",")
    return long(1000), (int(parts[0]), int(parts[1]), float(parts[2]))

def loadRows(sc, HomeDir):
    return sc.textFile(join(HomeDir, "output.txt")).map(parseWords)

def vectorize(rows, numWords):
    return rows.map(lambda x: (x[0], (x[1], x[2]))).groupByKey().mapValues(lambda x: SparseVector(numWords, x))

rows = loadRows(sc, HomeDir)
print "type of rows obj: ", type(rows)
print "count of rows: ", rows.count()
print "sample rating: ", rows.take(1)

#rows RDD:  (time stamp, (uid, mid, rows) )
#num of Books  (userid, wordID, rows)
numBooks = rows.values().map(lambda x: x[0]).max()+1   #num books
numWords = rows.values().map(lambda x: x[1]).max()+1  #num words

# ntransform into sparse vectors
"""
represent as sparse vector to save on space

three cols: id, vector size, movie:rating dictionary
size needed so u know how many zeros are in the mat?
uid, size of vector *around 3,000), (movie:rating, movie:rating, movie:rating))
"""


wordsSparseVector = vectorize( rows.values(), numWords)
print "wordsSparseVector Type:", type(wordsSparseVector)
print "wordsSparseVector Count:", wordsSparseVector.count()


#next: include a validation set. train on train, get errors on validation
#then: score == RMSE on the test set
minError = float("inf")
bestModel = None
bestK = None
test_values = [10, 20, 50, 100, 200]
error_storage = []
for i in test_values:
    model = KMeans.train(wordsSparseVector.values(), i, maxIterations = 20, runs = 10)
    #test this error on the validation set once we make that
    error = model.computeCost(wordsSparseVector.values())
    error_storage.append(error)
    if error < minError:
        bestModel = model
        minError = error
        bestK = i

"""
#save model once you have the best version
#model.save(sc, "KMeansModelCollaborative")
#model = KMeansModel.load(sc, "KMeansModelCollaborative")

#take one sample   the [0] is because this will be returned as a list -- not an index
user = wordsSparseVector(1)[0] #take a sample of 1 from the data set (use test data when doing this)
label = model.predict(user)   #outputs which cluster this user belongs to
# ==> a cluster id between 1 and k
clusterCenters = model.clusterCenters     #a list of centers (len == k)
clusterCenters[0] #len == total num of words, each obs == avg rating for people in this group
wordID = 4
print "predicted value: ", clusterCenters[label][wordID]
"""




#for i in range(10, 20):
# wordsSparseVector = > RDD where each item is ( userID , SparseVector)

##    if error < minError:
##        bestModel = model
##        minError = error
##        bestK = i
book = wordsSparseVector.values().take(1)[0] #take a sample of 1 from the data set (use test data when doing this)
print "Type book:", type(book)
print "Book id:", book

label = model.predict(book)   #outputs which cluster this user belongs to
clusterCenters = model.clusterCenters     #a list of centers (len == k)
#clusterCenters[0] #len == total num of words, each obs == avg rating for people in this group
print "Len Cluster Centers:", len(clusterCenters)
wordID = 4

print "predicted value: ", clusterCenters[label][wordID]   #movie id == word id, right? this should be book id though so let's figure this out

sc.stop()
