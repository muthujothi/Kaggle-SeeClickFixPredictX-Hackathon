#Motto : Make the model as simple as possible.

import csv
import numpy as np
from collections import Counter
from collections import OrderedDict
from collections import defaultdict
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
import pandas as pd

tag_numeral = 0
source_numeral = 0

tag_encode = dict()
source_encode = dict()

datareader = csv.reader(open('C:/LearningMaterials/Kaggle/SeeClickPredictX/train.csv','rb'))
header = datareader.next() #skip the header record.

#Numeratize the categorical variables : {tag_category,source_created}
for data in datareader:
    if data[10] not in tag_encode:
        tag_numeral = tag_numeral + 1
        tag_encode[data[10]] = tag_numeral
    if data[8] not in source_encode:
        source_numeral = source_numeral + 1
        source_encode[data[8]] = source_numeral

#Collect the features for the X_train dataset
X_train = []
y_views_train = []
y_votes_train = []
y_comments_train = []
data_count = 0
datareader = csv.reader(open('C:/LearningMaterials/Kaggle/SeeClickPredictX/train.csv','rb'))
header = datareader.next() #skip the header record.
for data in datareader:
    data_count = data_count + 1
    dates = pd.DatetimeIndex([data[9]])
    year = dates.year[0]
    month = dates.month[0]
    if data_count == 2:
        print X_train
    X_train.append(int(source_encode[data[8]])) #source_created
    X_train.append(int(tag_encode[data[10]])) #tag_category
    X_train.append(int(year)) #year
    X_train.append(int(month)) #month
    y_views_train.append((data[7])) #num_views
    y_votes_train.append((data[5])) #num_votes
    y_comments_train.append((data[6])) #num_comments

X_train =  np.array(X_train).reshape((data_count,4))
#y_views_train = np.array(y_views_train).reshape((data_count,1))
#y_votes_train = np.array(y_votes_train).reshape((data_count,1))
#y_comments_train = np.array(y_comments_train).reshape((data_count,1))

y_views_train = np.array(y_views_train)
y_votes_train = np.array(y_votes_train)
y_comments_train = np.array(y_comments_train)

print "Data ready for training..."
#Train the data on the RandomForestRegressor
forest_views = RandomForestRegressor(n_estimators=500)
forest_votes = RandomForestRegressor(n_estimators=500)
forest_comments = RandomForestRegressor(n_estimators=500)

forest_views = forest_views.fit(X_train,y_views_train)
forest_votes = forest_votes.fit(X_train,y_votes_train)
forest_comments = forest_comments.fit(X_train,y_comments_train)

#Now let us copy the code from the old flow to handle if one of the categorical variable is unavailable and go on tabulated prediction.
cat_votes = dict()
cat_comments = dict()
cat_views = dict()

all_votes = []
all_comments = []
all_views = []

cat_votes_median = dict()
cat_comments_median = dict()
cat_views_median = dict()

#votes --> data[5]
#comments --> data[6]
#views --> data[7]
#categorical tag - data[10]

#Look for Tag_Category+Source_created Combination. If that combination is not available, go by Source_created if the Category is 'NA'. Else go by Tag_Category.
#If none of these available then go by global values.
#Let us look at date and linear regression with regularization with tag_category, source_created, date, latitude and longitude as featue set.
datareader = csv.reader(open('C:/LearningMaterials/Kaggle/SeeClickPredictX/train.csv','rb'))
header = datareader.next() #skip the header record.
for data in datareader:

    votes = int(data[5])
    comments = int(data[6])
    views = int(data[7])
    
    all_votes.append(votes)
    all_comments.append(comments)
    all_views.append(views)
    
    if data[10] in cat_votes:
        cat_votes[data[10]].append(votes)
    else:
        cat_votes[data[10]] = [votes]

    if data[10] in cat_comments:
        cat_comments[data[10]].append(comments)
    else:
        cat_comments[data[10]] = [comments]

    if data[10] in cat_views:
        cat_views[data[10]].append(views)
    else:
        cat_views[data[10]] = [views]

    if data[8] in cat_votes:
        cat_votes[data[8]].append(votes)
    else:
        cat_votes[data[8]] = [votes]

    if data[8] in cat_comments:
        cat_comments[data[8]].append(comments)
    else:
        cat_comments[data[8]] = [comments]

    if data[8] in cat_views:
        cat_views[data[8]].append(views)
    else:
        cat_views[data[8]] = [views]

print "Global Median/Mode Votes"
arrayform_all_votes = np.asarray(all_votes)
#print np.amin(arrayform_all_votes)
counts = np.bincount(arrayform_all_votes)
gl_mode_votes = np.argmax(counts)
#print gl_mode_votes
#print "Global Median"
#print np.median(arrayform_all_votes)
#print "75th percentile.."
gl_median_votes = np.percentile(arrayform_all_votes,50)
#print gl_median_votes
#print "End -- Global Votes Mode.."

print "Use Global Median/mode Comments"
arrayform_all_comments = np.asarray(all_comments)
com_counts = np.bincount(arrayform_all_comments)
gl_mode_comments = np.argmax(com_counts)
gl_median_comments =  np.percentile(arrayform_all_comments,50)
#print gl_mode_comments
#print gl_median_comments

print "Use 75the percentile of global views"
arrayform_all_views = np.asarray(all_views)
vi_counts = np.bincount(arrayform_all_views)
gl_mode_views = np.argmax(vi_counts)
gl_median_views =  np.percentile(arrayform_all_views,75)
#print gl_mode_views
#print gl_median_views
    

print "Computing Category Votes mean..."
for key in cat_votes.iterkeys():
    arrayform_cat_votes = np.asarray(cat_votes[key])
    cat_median = np.percentile(arrayform_cat_votes,50)
    #cat_median = np.mean(arrayform_cat_votes)
    cat_votes_median[key] = cat_median


print "Computing Category Comments mean..."
for key in cat_comments.iterkeys():
    arrayform_cat_comments = np.asarray(cat_comments[key])
    cat_median = np.percentile(arrayform_cat_comments,50)
    #cat_median = np.mean(arrayform_cat_comments)
    cat_comments_median[key] = cat_median

print "Computing Category Views mean..."
for key in cat_views.iterkeys():
    arrayform_cat_views = np.asarray(cat_views[key])
    cat_median = np.percentile(arrayform_cat_views,50)
    #cat_median = np.mean(arrayform_cat_views)
    cat_views_median[key] = cat_median



datareader = csv.reader(open('C:/LearningMaterials/Kaggle/SeeClickPredictX/test.csv','rb'))
open_file_object = csv.writer(open("C:/LearningMaterials/Kaggle/SeeClickPredictX/submission.csv", "wb"))
header = datareader.next() #skip the first line of the test file.

#If both categorical features {tag_catgory,source_created} is available then use the Linear regressor.
#elif do whatever you did in the past code.
rand_forest_predictions = 0
total_records = 0
for data in datareader:

    data_views = gl_median_views
    data_votes = gl_mode_votes
    data_comments = gl_mode_comments
    total_records = total_records + 1

    dates = pd.DatetimeIndex([data[6]])
    year = dates.year[0]
    month = dates.month[0]
    predict_x = []
    if data[7] in tag_encode and data[5] in source_encode:
        rand_forest_predictions = rand_forest_predictions + 1
        predict_x.append(int(source_encode[data[5]])) #source_created
        predict_x.append(int(tag_encode[data[7]])) #tag_category
        predict_x.append(int(year)) #year
        predict_x.append(int(month)) #month
        reshaped_predict_x = np.array(predict_x).reshape((1,4))
        #print reshaped_predict_x
        data_views = round(forest_views.predict(reshaped_predict_x)[0],1)
        data_votes = round(forest_votes.predict(reshaped_predict_x)[0],1)
        data_comments = round(forest_comments.predict(reshaped_predict_x)[0],1)
    elif data[7] == 'NA' and data[5] in cat_views_median:
        data_views = int(cat_views_median[data[5]])
        data_votes = int(cat_votes_median[data[5]])
        data_comments = int(cat_comments_median[data[5]])
    else:
        if data[7] in cat_views_median:
            data_views = int(cat_views_median[data[7]])
            data_votes = int(cat_votes_median[data[7]])
            data_comments = int(cat_comments_median[data[7]])

    open_file_object.writerow([data[0],data_views,data_votes,data_comments])

print 'Total Test Records: \n', total_records
print 'RandomForestBasedPrediction: \n', rand_forest_predictions
print "Done..."









    
