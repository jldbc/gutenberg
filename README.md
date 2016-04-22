# Gutenberg
A Content Based Recommender using Project Gutenberg's entire database of books

Team:  
Aniket Saoji  
Drew Hoo  
James LeDoux  

-----------
## Feature Extraction
1. Run in terminal: MoreEfficientPreprocessing.py. This creates an output.txt with | delimeted features. Runs sentiment analysis, takes punctuation profile, gets other basic features.

## Run TFIDF clustering
1. Run in terminal: /[usr dir]/spark-submit /[usr dir]/tfidf.py "/[usr dir]/[data set input]/" "/[usr dir]/[output dir]"
  - Generated outputs = words_to_id.txt (txt file of every word in input data set \n separated), tfidf-scores-no-ids.csv (file format =    [bookID, Word, Score]), tfidf-scores.csv (same thing but with word ids instead of words for the clustering script)
2. Run topic clustering: /[usr dir]/spark-submit /[usr dir]/topic_clustering.py "/[usr dir]/[dir that contains output.txt]/". Outputs final-data.csv, which is the feature extraction data with cluster membership included. 



