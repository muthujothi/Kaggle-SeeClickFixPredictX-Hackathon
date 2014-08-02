import csv
import numpy as np
from collections import Counter
from collections import OrderedDict
from collections import defaultdict
from sklearn import linear_model

tag_numeral = 0
source_numeral = 0

tag_encode = dict()
source_encode = dict()

datareader = csv.reader(open('C:/LearningMaterials/Kaggle/SeeClickPredictX/subset_train.csv','rb'))
header = datareader.next() #skip the header record.

#Numeratize the categorical variables : {tag_category,source_created}
for data in datareader:
    if data[10] not in tag_encode:
        tag_numeral = tag_numeral + 1
        tag_encode[data[10]] = tag_numeral
    if data[8] not in source_encode:
        source_numeral = source_numeral + 1
        source_encode[data[8]] = source_numeral

print tag_encode
print source_encode

#Collect the features for the X_train dataset
X_train = []
Y1_train = [] #views
Y2_train = [] #votes
Y3_train = [] #comments
data_count = 0
datareader = csv.reader(open('C:/LearningMaterials/Kaggle/SeeClickPredictX/subset_train.csv','rb'))
for data in datareader:
    data_count = data_count + 1
    print data[1]


    
X_train = ((np.array(X_train,dtype='|S4')).astype(np.float)).reshape((data_count,4))
Y1_train = np.array(Y1_train).reshape((data_count,1))
Y2_train = np.array(Y2_train).reshape((data_count,1))
Y3_train = np.array(Y3_train).reshape((data_count,1))

print X_train
print "Create a Linear Regressor with Regularization Parameter."
regr_y1 = linear_model.RidgeCV(alphas=[0.001, 0.01, 0.1, 0.5, 0.75, 1.0])
regr_y2 = linear_model.RidgeCV(alphas=([0.001, 0.01, 0.1, 0.5, 0.75, 1.0]), fit_intercept=True, store_cv_values=True)
regr_y3 = linear_model.RidgeCV(alphas=([0.001, 0.01, 0.1, 0.5, 0.75, 1.0]), fit_intercept=True, store_cv_values=True)

print "Train the model to find the weights for fitting Y1.. Views"
regr_y1.fit(X_train, Y1_train)
print 'Coefficients for fitting num_views: \n', regr_y1.coef_
print 'CV on num_views: \n', regr_y1.cv_values_

print "Train the model to find the weights for fitting Y2.. Votes"
regr_y2.fit(X_train, Y2_train)
print 'Coefficients for fitting num_votes: \n', regr_y2.coef_
print 'CV on num_votes: \n', regr_y2.cv_values_

print "Train the model to find the weights for fitting Y3.. Views"
regr_y3.fit(X_train, Y3_train)
print 'Coefficients for fitting num_comments: \n', regr_y3.coef_
print 'CV on num_comments: \n', regr_y3.cv_values_

#######END OF LINEAR REGRESSION WITH REGRESSION MODEL##################
