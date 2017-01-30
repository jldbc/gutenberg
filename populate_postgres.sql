/*
Note: need to remove non-unicode observations before populating the db.
Locally I did this by filtering for those characters in excel and dropping those
rows. Put this into the preprocessing script before shipping to web app. 
*/
CREATE DATABASE gutenberg;
\connect gutenberg

CREATE TABLE features(
   id INT,
   file_name TEXT,
   total_words INT,
   avg_sentence_size REAL,
   exclamation REAL,
   pound_sign REAL,
   quotes REAL,
   pct_sign REAL,
   dollar_sign REAL,
   and_symbol REAL,
   parentheses REAL,
   plus_sign REAL,
   asterisk REAL,
   dash REAL,
   comma REAL,
   backslash REAL,
   period REAL,
   semicolon REAL,
   colon REAL,
   equals_sign REAL,
   lessthan REAL,
   question_mark REAL,
   at_symbol REAL,
   bracket REAL,
   underscore REAL,
   upward_carrot REAL,
   apostrophe REAL,
   squiggle_bracket REAL,
   tilde REAL,
   neg REAL,
   neu REAL,
   pos REAL,
   compound REAL,
   title TEXT,
   author TEXT);


COPY features(id,file_name, total_words, avg_sentence_size, exclamation, pound_sign, quotes, pct_sign, dollar_sign, and_symbol, parentheses, plus_sign, asterisk, dash, comma, backslash, period, semicolon, colon, equals_sign, lessthan, question_mark, at_symbol, bracket, underscore, upward_carrot, apostrophe, squiggle_bracket, tilde, neg, neu, pos, compound, title, author) 
FROM '/Users/jamesledoux/Documents/gutenberg/features_attempt.csv' 
DELIMITER ',' 
ENCODING 'UTF8'
CSV HEADER;

select * from feats_full_test where author = 'William Shakespeare';

