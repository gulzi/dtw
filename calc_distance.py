import math
import numpy as np

def ecludian_distance(ts1,ts2):
    x = np.array(ts1)
    y = np.array(ts2)
    sum = 0.0
    if x.size > y.size:
        
        for i in range(0,y.size):
            sum = sum + pow(x[i]-y[i],2)
        return math.sqrt(sum)
    elif x.size > 1:
        for i in range(0,x.size):
            sum = sum + pow(x[i]-y[i],2)
        return math.sqrt(sum)
    else:
        return math.sqrt(pow(x-y,2))
        # to do: throw exception/error if to keep size equal
        #print("cannot calculate ecludian distance since size of time series are not same")
        #return None

def manhattan_distance(ts1,ts2):
    x = np.array(ts1)
    y = np.array(ts2)
    
    return abs(x-y) 