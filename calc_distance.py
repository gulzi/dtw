import math
import numpy as np

def ecludian_distance(ts1,ts2):

    sum = 0.0
    if ts1.size > ts2.size:
        
        for i in range(0,ts2.size):
            sum = sum + math.pow(ts1[i]-ts2[i],2)
        return math.sqrt(sum)
    else:
        for i in range(0,ts1.size):
            sum = sum + math.pow(ts1[i]-ts2[i],2)
        return math.sqrt(sum)
        # to do: throw exception/error if to keep size equal
        #print("cannot calculate ecludian distance since size of time series are not same")
        #return None
