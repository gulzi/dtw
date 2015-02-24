import math
import numpy as np


               
def shrunk_timeseries(ts,shrunk_size=0):
    print(shrunk_size)
    print(ts.size)
    if shrunk_size > ts.size or shrunk_size <= 0:
        return shrunk_size
    result = np.zeros(shrunk_size)
    print(result)
    reduced_pt_size = ts.size/shrunk_size
    read_from = 0
    read_to = 0
    instert_to_result = 0
    
    while read_from < ts.size:
        
        read_to = round(reduced_pt_size*(instert_to_result+1))-1
        print("read from",read_from)
        print("read to",read_to)
        no_of_pts_to_read = read_to - read_from+1
        
        # time_sum is not needed for now
        #time_sum = 0.0
        agg_points_sum = 0.0

        for i in range(read_from,read_to+1):
            print("counter i:",i)
            current_point = ts[i]
            agg_points_sum = agg_points_sum + current_point
        
        agg_points_sum  = agg_points_sum / no_of_pts_to_read
        result[instert_to_result] = agg_points_sum

        read_from = read_to +1
        instert_to_result = instert_to_result +1
    return result
        # throw error/exception
        
def shrunk_short(ts):
    i = 0
    result = np.zeros(ts.size/2)
    result_index = 0
    while(i < ts.size):
        print(i)
        result[result_index] = (ts[i]+ts[i+1])/2
        result_index = result_index +1
        i = i + 2
    
    return result
