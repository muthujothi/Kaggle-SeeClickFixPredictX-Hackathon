import csv
import numpy as np
from collections import Counter
from collections import OrderedDict
from collections import defaultdict


datareader = csv.reader(open('C:/LearningMaterials/Kaggle/SeeClickPredictX/train.csv','rb'))
header = datareader.next() #skip the first line

#Seeing how many specific cases had been reported under any specific category
#categoryCounter = Counter()
#for data in datareader:
#    categoryCounter[data[10]] += 1

#dictCatReports = OrderedDict(sorted(categoryCounter.items(), key=lambda t: (t[0])))

#for k,v in dictCatReports.items():
#    print k,v
#Seeing how many specific cases had been reported under any specific category

cat_votes = dict()
cat_comments = dict()
cat_views = dict()

cat_source_votes = dict()
cat_source_comments = dict()
cat_source_views = dict()


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

    if data[10]+data[8] in cat_votes:
        cat_votes[data[10]+data[8]].append(votes)
    else:
        cat_votes[data[10]+data[8]] = [votes]

    if data[10]+data[8] in cat_comments:
        cat_comments[data[10]+data[8]].append(comments)
    else:
        cat_comments[data[10]+data[8]] = [comments]

    if data[10]+data[8] in cat_views:
        cat_views[data[10]+data[8]].append(views)
    else:
        cat_views[data[10]+data[8]] = [views]


print "Global Median/Mode Votes"
arrayform_all_votes = np.asarray(all_votes)
#print np.amin(arrayform_all_votes)
counts = np.bincount(arrayform_all_votes)
gl_mode_votes = np.argmax(counts)
print gl_mode_votes
#print "Global Median"
#print np.median(arrayform_all_votes)
#print "75th percentile.."
gl_median_votes = np.percentile(arrayform_all_votes,50)
print gl_median_votes
#print "End -- Global Votes Mode.."

print "Use Global Median/mode Comments"
arrayform_all_comments = np.asarray(all_comments)
com_counts = np.bincount(arrayform_all_comments)
gl_mode_comments = np.argmax(com_counts)
gl_median_comments =  np.percentile(arrayform_all_comments,50)
print gl_mode_comments
print gl_median_comments

print "Use 75the percentile of global views"
arrayform_all_views = np.asarray(all_views)
vi_counts = np.bincount(arrayform_all_views)
gl_mode_views = np.argmax(vi_counts)
gl_median_views =  np.percentile(arrayform_all_views,75)
print gl_mode_views
print gl_median_views
    

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

#print "How on a median scale people view a category 311 issue?"
#for k,v in cat_views_median.items():
#    print k,v


datareader = csv.reader(open('C:/LearningMaterials/Kaggle/SeeClickPredictX/test.csv','rb'))
open_file_object = csv.writer(open("C:/LearningMaterials/Kaggle/SeeClickPredictX/submission.csv", "wb"))
header = datareader.next() #skip the first line of the test file.

for data in datareader:
    data_views = int(gl_median_views)
    data_votes = int(gl_mode_votes)
    data_comments = int(gl_mode_comments)

    if data[7]+data[5] in cat_views_median:
        data_views = int(cat_views_median[data[7]+data[5]])
    elif data[7] == 'NA' and data[5] in cat_views_median:
        data_views = int(cat_views_median[data[5]])
    else:
        if data[7] in cat_views_median:
            data_views = int(cat_views_median[data[7]])
        
    if data[7]+data[5] in cat_votes_median:
        data_votes = int(cat_votes_median[data[7]+data[5]])
    elif data[7] == 'NA' and data[5] in cat_votes_median:
        data_votes = int(cat_votes_median[data[5]])
    else:
        if data[7] in cat_votes_median:
            data_votes = int(cat_votes_median[data[7]])


    if data[7]+data[5] in cat_comments_median:
        data_comments = int(cat_comments_median[data[7]+data[5]])
    elif data[7] == 'NA' and data[5] in cat_comments_median:
        data_comments = int(cat_comments_median[data[5]])
    else:
        if data[7] in cat_comments_median:
            data_comments = int(cat_comments_median[data[7]])

    open_file_object.writerow([data[0],data_views,data_votes,data_comments])

print "done..."
#try:
#    import pandas
#    print "Pandas installed"
#except ImportError:
#    print "Pandad not installed"
