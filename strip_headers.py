import os
import time
start_time = time.clock()

start_list = ("*** START OF", "***START OF")

stop_list = ("*** END OF", "***END OF", "End of the Project")



directory = "/Users/jamesledoux/Documents/gutenberg_big_data/"
outputdir = "/Users/jamesledoux/Documents/gutenberg_big_data_better"
for book in os.listdir(directory):
  if not book.startswith("."):
    with open(directory + book) as f:
      content = f.readlines()
    start_index = 1
    stop_index = len(content) - 1
    for line in range(len(content)):
      #if start1 or start2 in content[line]:
      if any(item in content[line] for item in start_list):
        start_index = line + 1
      #if stop1 or stop2 or stop3 in content[line]:
      if any(item in content[line] for item in stop_list):
        stop_index = line - 2
    book_content = content[start_index:stop_index]
    outfile = open(outputdir + '/' + book, 'w')
    outfile.writelines(book_content)
    outfile.close()

end_time = time.clock()
total_time = end_time - start_time
print "The total time: ", total_time

        
        
        
        
    