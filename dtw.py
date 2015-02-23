from pandas.io.data import DataReader
from datetime import datetime
from numpy  import *
from util import *

f = DataReader("F",  "yahoo", datetime(2000,1,1), datetime(2012,1,1))

f_2008=f[f.index.year==2008]
f_2009=f[f.index.year==2009]

ts1 = array(f_2009.Volume.values)
ts2 = array(f_2008.Volume.values)

distance = calculate_ecludian_distance(ts1,ts2)
