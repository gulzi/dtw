import math
import numpy as np


               
def shrunk_timeseries(ts,shrunk_size=0):

    if shrunk_size > ts.size or shrunk_size <= 0:
        return shrunk_size # return error
    shrunked = np.zeros(shrunk_size)
    reduced_pt_size = ts.size/shrunk_size
    read_from = 0
    read_to = 0
    instert_to_result = 0
    agg_point_size = np.zeros(shrunk_size,dtype=np.int)
    while read_from < ts.size:
        
        read_to = round(reduced_pt_size*(instert_to_result+1))-1
        no_of_pts_to_read = read_to - read_from+1
        
        # time_sum is not needed for now
        #time_sum = 0.0
        agg_points_sum = 0.0
        i = read_from
        #for i in range(read_from,read_to):
        while i <= read_to and read_to < ts.size:
            try:
                current_point = ts[i]
            except IndexError:    
                current_point = ts[i-1]
                
            agg_points_sum = agg_points_sum + current_point
            i = i +1
        
        agg_points_sum  = agg_points_sum / no_of_pts_to_read
        shrunked[instert_to_result] = agg_points_sum
        agg_point_size[instert_to_result] = no_of_pts_to_read
        read_from = read_to +1
        if read_to < ts.size-1:
            instert_to_result = instert_to_result +1
        
        
    return shrunked,agg_point_size
        # throw error/exception
        
def shrunk_short(ts):
    i = 0
    result = np.zeros(ts.size/2)
    result_index = 0
    while(i < ts.size):
        result[result_index] = (ts[i]+ts[i+1])/2
        result_index = result_index +1
        i = i + 2
    
    return result

