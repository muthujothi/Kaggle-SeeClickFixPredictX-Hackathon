#summary = 'brush & trimmings ###### BBB' 
#if "brush" or "Brush" in summary:
#    print "Hello NLP..."

import csv
import numpy as np
from collections import Counter
from collections import OrderedDict
from collections import defaultdict
import pandas as pd

datareader = csv.reader(open('C:/LearningMaterials/Kaggle/SeeClickPredictX/train.csv','rb'))
header = datareader.next() #skip the first line

cat_votes = dict()
cat_comments = dict()
cat_views = dict()

all_votes = []
all_comments = []
all_views = []

cat_votes_median = dict()
cat_comments_median = dict()
cat_views_median = dict()

cat_views_timebased = dict()
#votes --> data[5]
#comments --> data[6]
#views --> data[7]
#categorical tag - data[10]

for data in datareader:

    votes = int(data[5])
    comments = int(data[6])
    views = int(data[7])

    all_votes.append(votes)
    all_comments.append(comments)
    all_views.append(views)

    tag_category = data[10] #issue_type
    source_generated = data[8] #medium of issue reporting
    summary = data[3] #summary of the issue reported

    dates = pd.DatetimeIndex([data[9]])
    year = dates.year[0]
    month = dates.month[0]
    
    if tag_category == 'NA':
        if "brush" or "Brush" in summary:
            tag_category = "brush"
        elif "Graffiti" or "graffiti" in summary:
            tag_category = "graffiti"
        elif "Street Light" in summary:
            tag_category = "street_light"
        elif "furniture" in summary:
            tag_category = "furniture"
        elif "Alley Light" in summary:
            tag_category = "Alley Light Out"
        elif "Building Violation" in summary:
            tag_category = "Building Violation"
        elif ("bulk" or "Bulk" in summary )and ("brush" or "Brush" not in summary):
            tag_category = "bulk"
        elif "limbs" in summary:
            tag_category = "limbs"
        elif "Litter" or "litter" in summary:
            tag_category = "Litter"
        elif "lost" or "Lost" or "LOST" in summary:
            tag_category = "lost"
        elif "mattress" or "Mattress" in summary:
            tag_category = "Mattress"
        elif "Pavement" in summary:
            tag_category = "Pavement"
        elif "Pothole" in summary:
            tag_category = "pothole"
        elif "Rodent" in summary:
            tag_category = "rodent"
        elif "Sanitation" in summary:
            tag_category = "sanitation"
        elif "Trim" in summary:
            tag_category = "trim"

    if tag_category == 'abandoned_vehicle':
        tag_category = "abandoned_vehicles"
            
    latitude = str((str(data[1])).split(".")[0])
    longitude = str((str(data[2])).split(".")[0])

    if latitude == '37' and longitude == '-77':
        city = 'Richmond'
    elif latitude == '37' and longitude == '-122':
        city = 'Oakland'
    elif latitude == '41' and longitude == '-72':
        city = 'NewHaven'
    else:
        city = 'Chicago'
    
    if tag_category in cat_votes:
        cat_votes[tag_category].append(votes)
    else:
        cat_votes[tag_category] = [votes]

    if tag_category in cat_comments:
        cat_comments[tag_category].append(comments)
    else:
        cat_comments[tag_category] = [comments]

    if tag_category in cat_views:
        cat_views[tag_category].append(views)
    else:
        cat_views[tag_category] = [views]

    if source_generated in cat_votes:
        cat_votes[source_generated].append(votes)
    else:
        cat_votes[source_generated] = [votes]

    if source_generated in cat_comments:
        cat_comments[source_generated].append(comments)
    else:
        cat_comments[source_generated] = [comments]

    if source_generated in cat_views:
        cat_views[source_generated].append(views)
    else:
        cat_views[source_generated] = [views]

    #Start of city_reported
    if city in cat_votes:
        cat_votes[city].append(votes)
    else:
        cat_votes[city] = [votes]

    if city in cat_comments:
        cat_comments[city].append(comments)
    else:
        cat_comments[city] = [comments]

    if city in cat_views:
        cat_views[city].append(views)
    else:
        cat_views[city] = [views]
    #End of city_reported

    #Start of MonthYear_reported
    if month+year in cat_votes:
        cat_votes[month+year].append(votes)
    else:
        cat_votes[month+year] = [votes]

    if month+year in cat_comments:
        cat_comments[month+year].append(comments)
    else:
        cat_comments[month+year] = [comments]

    if month+year in cat_views:
        cat_views[month+year].append(views)
    else:
        cat_views[month+year] = [views]
    #End of MonthYear_reported

    #cat_views_timebased
    if month+year in cat_views_timebased:
        cat_views_timebased[month+year].append(views)
    else:
        cat_views_timebased[month+year] = [views]  

#print cat_votes['brush']
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
    #cat_median = np.percentile(arrayform_cat_votes,50)
    #cat_median = np.mean(arrayform_cat_votes)
    counts = np.bincount(arrayform_cat_votes)
    cat_median = np.argmax(counts)
    cat_votes_median[key] = cat_median


print "Computing Category Comments mean..."
for key in cat_comments.iterkeys():
    arrayform_cat_comments = np.asarray(cat_comments[key])
    #cat_median = np.percentile(arrayform_cat_comments,50)
    #cat_median = np.mean(arrayform_cat_comments)
    counts = np.bincount(arrayform_cat_comments)
    cat_median = np.argmax(counts)
    cat_comments_median[key] = cat_median

print "Computing Category Views mean..."
for key in cat_views.iterkeys():
    arrayform_cat_views = np.asarray(cat_views[key])
    #cat_median = np.percentile(arrayform_cat_views,50)
    #cat_median = np.mean(arrayform_cat_views)
    counts = np.bincount(arrayform_cat_views)
    cat_median = np.argmax(counts)
    cat_views_median[key] = cat_median

print "Computing Category Views mean timebased..."
cat_view_time_mean = dict()
for key in cat_views_timebased.iterkeys():
    arrayform_cat_views = np.asarray(cat_views_timebased[key])
    #cat_median = np.percentile(arrayform_cat_views,50)
    cat_median = np.mean(arrayform_cat_views)
    #counts = np.bincount(arrayform_cat_views)
    #cat_median = np.argmax(counts)
    cat_view_time_mean[key] = cat_median

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

    tag_category = data[7]
    source_created = data[5]
    summary = data[3] #summary of the issue reported
    
    if tag_category == 'NA':
        if "brush" or "Brush" in summary:
            tag_category = "brush"
        elif "Graffiti" or "graffiti" in summary:
            tag_category = "graffiti"
        elif "Street Light" in summary:
            tag_category = "street_light"
        elif "furniture" in summary:
            tag_category = "furniture"
        elif "Alley Light" in summary:
            tag_category = "Alley Light Out"
        elif "Building Violation" in summary:
            tag_category = "Building Violation"
        elif ("bulk" or "Bulk" in summary )and ("brush" or "Brush" not in summary):
            tag_category = "bulk"
        elif "limbs" in summary:
            tag_category = "limbs"
        elif "Litter" or "litter" in summary:
            tag_category = "Litter"
        elif "lost" or "Lost" or "LOST" in summary:
            tag_category = "lost"
        elif "mattress" or "Mattress" in summary:
            tag_category = "Mattress"
        elif "Pavement" in summary:
            tag_category = "Pavement"
        elif "Pothole" in summary:
            tag_category = "pothole"
        elif "Rodent" in summary:
            tag_category = "rodent"
        elif "Sanitation" in summary:
            tag_category = "sanitation"
        elif "Trim" in summary:
            tag_category = "trim"

    if tag_category == 'abandoned_vehicle':
        tag_category = 'abandoned_vehicles'

    latitude = str((str(data[1])).split(".")[0])
    longitude = str((str(data[2])).split(".")[0])

    if latitude == '37' and longitude == '-77':
        city = 'Richmond'
    elif latitude == '37' and longitude == '-122':
        city = 'Oakland'
    elif latitude == '41' and longitude == '-72':
        city = 'NewHaven'
    else:
        city = 'Chicago'

    dates = pd.DatetimeIndex([data[6]])
    year = dates.year[0]
    month = dates.month[0]

    if tag_category in cat_views_median:
        data_views = int(cat_views_median[tag_category])
        data_votes = int(cat_votes_median[tag_category])
        data_comments = int(cat_comments_median[tag_category])
    elif source_created in cat_views_median:
        data_views = int(cat_views_median[source_created])
        data_votes = int(cat_votes_median[source_created])
        data_comments = int(cat_comments_median[source_created])
    elif city in cat_views_median:
        data_views = int(cat_views_median[city])
        data_votes = int(cat_votes_median[city])
        data_comments = int(cat_comments_median[city])
    
    if tag_category == 'NA' and month+year in cat_view_time_mean:
        data_views = round(cat_view_time_mean[month+year],1)

    open_file_object.writerow([data[0],data_views,data_votes,data_comments])
#print cat_views_median['2012']
print "done..."

















