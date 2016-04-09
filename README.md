# Gutenberg
A Content Based Recommender using Project Gutenberg's entire database of books

Team:  
Aniket Saoji  
Drew Hoo  
James LeDoux  

-----------
## Run TFIDF clustering
1. Run in terminal: /[usr dir]/spark-submit /[usr dir]/tfidf.py "/[usr dir]/[data set input]/" "/[usr dir]/[output dir]"
2. Generated outputs = words_to_id.txt (txt file of every word in input data set \n separated), tfidf-scores.csv (file format = [bookID, Word, Score])
3. Run reformatting.py => No command line inputs, need to adjust filepaths inside .py file: (line 3: lista, line 13: file_name)
4. Ouput of reformatting is "output.csv" NOTE: 4/3/16 need to change that
5. Now run Topic Clustering: /[usr dir]/spark-submit /[usr dir]/topic_clustering.py "/[usr dir]/[dir that contains output.txt]/"
NOTE: 4/3/16 => output.csv needs to be changed to output.txt in order to run in topic clustering
