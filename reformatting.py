import csv

lista = open('/Users/jamesledoux/Documents/BigData/gutenberg/words_to_id.txt').read().splitlines()
lista = sorted(lista)

#populate {word: id} dictionary for lookups / swaps
IDs = {}
j = 0
for i in lista:
    IDs[i] = j
    j = j+1

file_name = '/Users/jamesledoux/Documents/BigData/gutenberg/TFIDF Output/tfidf-scores.csv'
with open(file_name, 'r') as f:
    reader = csv.reader(f)
    data = list(list(row) for row in csv.reader(f, delimiter=',')) #reads csv into a list of lists

for row in data:
  #swap book title for book title ID
  row[1] = IDs[row[1]]

with open("output.csv", "wb") as f:
    writer = csv.writer(f)
    writer.writerows(data)

f.close()
