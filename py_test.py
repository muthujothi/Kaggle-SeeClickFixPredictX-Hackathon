import numpy as np
import scipy

S1 = 'NA'
if S1 == 'NA':
    print "Worlddd"
else:
    print "sorry..."


x = np.arange(9)
x.shape = (3,3)
#[[0 1 2]
# [3 4 5]
# [6 7 8]]

#print x[2:]
print x[:2]

import pandas as pd
dates = pd.DatetimeIndex(['2013-01-01 00:01:30'])
print dates.year[0]
print dates.month[0]

lat = '-122.202391'
print lat.split(".")[0]
