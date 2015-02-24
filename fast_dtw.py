from pandas.io.data import DataReader
from datetime import datetime
from numpy  import *
from util import *

f = DataReader("F",  "yahoo", datetime(2000,1,1), datetime(2012,1,1))

f_2008=f[f.index.year==2008]
f_2009=f[f.index.year==2009]

X = array(f_2009.Volume.values)
Y = array(f_2008.Volume.values)

#ts1 = shrunk_short(ts1)
#print(ts1)
#print(ts1.size)
#print(ts.size)

def fast_dtw(ts1,ts2,radius,distance):
    radius if radius > 0 else 0
    
    min_t_size = radius +2
    # set resolution factor
    resolation_factor = 2
    #base case for recursive call
    if ts1.size <= min_t_size or ts2.size <= min_t_size:
        return
    
    # shrunk time series
    shrunk_x = shrunk_timeseries(X,X.size/resolation_factor) 
    shrunk_y = shrunk_timeseries(Y,Y.size/resolation_factor)
    
    
    '''
    
    # call recursively on every shrunked time series
    # return dtw calculations

'''
