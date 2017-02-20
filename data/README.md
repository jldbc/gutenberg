# Dataset Description

This folder has two data sets. The two differences between the data sets are that one has more observations than the other (~23,000 vs. ~43,000 rows), and that the smaller dataset includes cluster IDs based on k-means models run on the books' vectors of TF-IDF scores. Besides these two differences, the datasets' other features are identical to one another. 

Each observation is a book taken from Project Gutenberg, and each column is a feature taken while parsing the files. Most of the columns are punctuation frequencies (there are 30 of these), but the data also includes content clusters, sentiment scores, and average word length. Eventually, I'm hoping to add part-of-speech tagging. 

## Features 

* **book_name**
* **author**
* **total_words**
* **avg_sentence_length**
* **punctuation marks:** any feature whose name is a punctuation mark (e.g. '!', '?', '[', etc.) is that punctuation mark's usage frequency in that text, relative to the text's overall puncuation usage. For a question mark, this is defined as (number_of_question_marks/total_number_of_punctuation_marks)
* **neg:** negative sentiment score 
* **neu:** neutral sentiment score
* **pos:** positive sentiment score
* **compound:** compound sentiment score
* **SmallClusterID:** cluster IDs from KMeans model with small k (k=50)
* **MediumClusterID:** cluster IDs from KMeans model with medium-sized k (k=155)
* **LargeClusterID:** cluster IDs from KMeans model with large k (k=480)


Note: sentiment analysis tool was NLTK's VADER model. See [here](http://www.nltk.org/howto/sentiment.html) for details. 