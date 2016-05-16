import pandas as pd 
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import MinMaxScaler
"""
data preparation:
drop duplicate features that have pairs (e.g. open and closed parentheses, left & right bracket, etc.)
Create author and cluster dummies 
Save author and title names (so we can describe our predictions to a user) and then drop them (since they are string data)

Scale the data to [0,1] scale by subtracting mins and then dividing by max-min
"""

"""
feature count:
original: 39
with author dummies: 9813
with cluster dummies: 9863 => 10018 => 10498
39 general punctuation / metadata features, >9,800 author binary variables, >650 clustering features
"""

"""
data = pd.read_csv("/Users/jamesledoux/Desktop/all-data.csv")
data = data.drop('>', 1)
data = data.drop('(', 1)
data = data.drop('[', 1)
data = data.drop('{', 1)
data = pd.concat([data, pd.get_dummies(data['author'])], axis=1)   #now you have a binary variable for each author
data = pd.concat([data, pd.get_dummies(data['smallClusterId'], prefix="general")], axis=1)  #and for each cluster
data = pd.concat([data, pd.get_dummies(data['mediumClusterId'], prefix="medium")], axis=1) 
data = pd.concat([data, pd.get_dummies(data['largeClusterId'], prefix="specific")], axis=1) 
data = data.drop('smallClusterId', 1)
data = data.drop('mediumClusterId', 1)
data = data.drop('largeClusterId', 1)
"""

data = pd.read_csv('/Users/jamesledoux/Desktop/ols_data.csv')
authors = data['author']
titles = data['book_name']  
IDs = data['ID']
data = data.drop('ID', 1)


data = data.drop('filename', 1)
data = data.drop('author', 1)
data = data.drop('book_name', 1)

#replace NAs 
data = data.fillna(value=0)

#scale the data 
scaler = MinMaxScaler()
data = pd.DataFrame(scaler.fit_transform(data), columns=data.columns)
data['ID'] = IDs  #had to remove this earlier because we didn't want IDs to be scaled with the other columns 


"""
some test ratings sets we came up with. our personal ratings
#aniket
id_list = [120, 43, 174, 30975, 1998, 12454, 514, 1250, 32325, 34117, 28464, 23042, 27761, 2916,4195, 2600, 11224, 12138, 12162, 12290, 12486]
user_ratings = [10, 10, 10, 2, 8, 2, 7, 9, 10, 10, 1, 8, 8, 9, 1, 3, 3, 1, 1, 1, 1]

#james 
id_list = [996, 27761, 22791, 228, 150, 25344, 28464, 19211, 4217, 8800, 1400, 2009, 32325, 91, 102, 219, 11224, 2701, 32573, 10807, 26955, 23043]
user_ratings = [10, 10, 10, 8, 2, 5, 1, 2, 10, 7, 7, 3, 9,10, 9, 8, 5, 4,1, 1, 1, 9]
"""

id_list = [996, 27761, 22791, 228, 150, 25344, 28464, 19211, 4217, 8800, 1400, 2009, 32325, 91, 102, 219, 11224, 2701, 32573, 10807, 26955, 23043]

user_ratings = [10, 10, 10, 8, 2, 5, 1, 2, 10, 7, 7, 3, 9,10, 9, 8, 5, 4,1, 1, 1, 9]

train_x = data[data['ID'].isin(id_list)]
train_x['y'] = 5   #a default starting value. this will be updated to the actual ratings.

#these go in the wrong order since the id_list is not in order when creating the df. fix this by looping/updating ratings
for i in range(len(id_list)):
    val = id_list[i]
    train_x.loc[train_x['ID'] == val, 'y'] = user_ratings[i]


train_y = train_x['y']
train_x = train_x.drop('y', 1)

trainIDs = train_x['ID']
train_x = train_x.drop('ID', 1)   #because id should not be interpted as a feature 


model = LinearRegression()
model = model.fit(train_x, train_y)
data = data.drop('ID', 1)  #full id list saved as IDs, use this if needed later
predicted_ratings = model.predict(data)
data['preds'] = predicted_ratings 	
data['book_name'] = titles
data['author'] = authors
best_recommendations = data[['book_name','author', 'preds']]
best_recommendations = best_recommendations.sort(['preds'], ascending = False)
best_recommendations.head(25)



#find a way to exclude ones in the training data. seeing books you already rated is not useful
