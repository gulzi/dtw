import numpy as np
from decimal import Decimal
import calc_distance as dist
import calc_distance
from numpy import Infinity



def dtw(ts_x,ts_y):
    
    cost_matrix = np.empty([ts_x.size,ts_y.size])
    
    max_x = ts_x.size -1
    max_y = ts_y.size -1
    cost_matrix[0][0] = dist.ecludian_distance(ts_x[0],ts_y[0])
    
    for j in range(1,max_y+1):
        cost_matrix[0][j] = cost_matrix[0][j-1] + dist.ecludian_distance(ts_x[0],ts_y[j])
        
    
    for i in range(1,max_x+1): 
        cost_matrix[i][0] = cost_matrix[i-1][0] + dist.ecludian_distance(ts_x[i],ts_y[0])
        
        for j in range(1,max_y+1):
            min_global = min(cost_matrix[i-1][j],min(cost_matrix[i-1][j-1],cost_matrix[i][j-1]))
            cost_matrix[i][j] = min_global + dist.ecludian_distance(ts_x[i],ts_y[j])
    
            
    minimum_cost = cost_matrix[max_x][max_y]
    if max_x == max_y:        
        minimum_cost_path = np.empty(max_x+1, dtype='int8, int8')
    elif max_x < max_y:
        minimum_cost_path = np.empty(max_y+1, dtype='int8, int8')
    else:
        minimum_cost_path = np.empty(max_x+1, dtype='int8, int8')
            
    minimum_cost_path[:] = -1
    i,j = max_x,max_y
    minimum_cost_index = minimum_cost_path.size -1
    minimum_cost_path[minimum_cost_index] = (i,j)
    
    while i >0 or j >0:
        diag_cost = Decimal('Infinity')
        left_cost = Decimal('Infinity')
        down_cost = Decimal('Infinity')
        
        if (i > 0) and (j > 0): 
            diag_cost = cost_matrix[i-1][j-1]
        if i > 0: 
            left_cost = cost_matrix[i-1][j]
        if j > 0:             
            down_cost = cost_matrix[i][j-1]
        
        if (diag_cost <= left_cost and diag_cost <= down_cost):
            i = i-1
            j = j-1
        elif (left_cost < diag_cost and left_cost < down_cost):
            i = i-1
        elif (down_cost<diag_cost and down_cost<left_cost):
            j = j -1
        elif i <= j:
            j = j -1
        else:
            i = i-1
        minimum_cost_index = minimum_cost_index -1
        minimum_cost_path[minimum_cost_index] = (i,j)
        
        
    return minimum_cost,minimum_cost_path


def search_window(ts1,ts2,shrunk1,shrunk2,warp_path,radius,agg_point_size_x,agg_point_size_y):
    
    min_values = np.empty(ts1.size)
    min_values[:] = -1
    max_values = np.zeros(ts1.size)
    max_j = ts2.size-1
    size = 0
    mod_count = 0
    
    current_i,current_j = warp_path[0]
    
    last_warp_i = Decimal('Infinity')
    last_warp_j = Decimal('Infinity')
    
    
    for w in range(0,warp_path.size):
        warped_i,warped_j = warp_path[w]
        
        block_size_for_i = agg_point_size_x[warped_i]
        block_size_for_j = agg_point_size_y[warped_j]
        
        if warped_j > last_warp_j:
            current_j = current_j + agg_point_size_y[last_warp_j]
        
        if warped_i > last_warp_i:
            current_i = current_i + agg_point_size_x[last_warp_i]
                
        
        if (warped_j > last_warp_j) and (warped_i > last_warp_i):
            min_values,max_values,size,mod_count = mark_visited(min_values, max_values, size, mod_count,current_i - 1 , current_j)
            min_values,max_values,size,mod_count = mark_visited(min_values, max_values, size, mod_count,current_i , current_j - 1)
        
        for x in range(0,block_size_for_i):
            min_values,max_values,size,mod_count = mark_visited(min_values, max_values, size, mod_count,current_i + x , current_j)
            min_values,max_values,size,mod_count = mark_visited(min_values, max_values, size, mod_count,current_i + x , current_j+block_size_for_j-1)
            
        last_warp_i = warped_i
        last_warp_j = warped_j
    
    return expand_window(min_values,max_values,size,mod_count,max_j,radius)         

def expand_window(min_values,max_values,size,mod_count,max_j,radius):
    if radius > 0:
        min_values,max_values,size,mod_count = expand_search_window(min_values,max_values,size,mod_count,max_j,1)
        return expand_search_window(min_values,max_values,size,mod_count,max_j,radius-1)

def expand_search_window(min_values,max_values,size,mod_count,max_j,radius):
    if radius > 0:
        window_cells = np.full(size,fill_value=-1, dtype='int8, int8')
        next_val = True
        current_i = 0
        current_j = 0
        counter = 0
        min_i = 0
        min_j = 0
        max_i = min_values.size - 1
        
        while next_val == True:
            window_cells[counter] = (current_i,current_j)
            current_j = current_j + 1
            if current_j > max_values[current_i]:
                current_i = current_i +1
                if current_i <= (min_values.size -1):
                    current_j = min_values[current_i]
                else:
                    next_val = False
            counter = counter + 1
        
        for cell in range(0,window_cells.size):
            cell_col, cell_row = window_cells[cell]
            
            if cell_col != min_i and cell_row != max_j:
                target_col = cell_col - radius
                target_row = cell_row + radius
                
                if (target_col >= min_i) and (target_row <= max_j):                
                    min_values,max_values,size,mod_count = mark_visited(min_values, max_values, size, mod_count, target_col, target_row)
                    
                else:                
                    cells_past_edge = max(min_i-target_col,target_row-max_j)
                    min_values,max_values,size,mod_count = mark_visited(min_values, max_values, size, mod_count, target_col+cells_past_edge, target_row-cells_past_edge)
                
            if cell_row != max_j:
                target_col = cell_col
                target_row = cell_row + radius
                
                if target_row <= max_j:
                    min_values,max_values,size,mod_count = mark_visited(min_values, max_values, size, mod_count, target_col, target_row)   
                else:
                    cells_past_edge = target_row-max_j
                    min_values,max_values,size,mod_count = mark_visited(min_values, max_values, size, mod_count, target_col, target_row-cells_past_edge)
                     
            if (cell_col != max_i) and (cell_row != max_j):
                target_col = cell_col + radius
                target_row = cell_row + radius
                
                if target_col <= max_i and target_row <= max_j:
                    min_values,max_values,size,mod_count = mark_visited(min_values, max_values, size, mod_count, target_col,target_row)
                    
                else:
                    cells_past_edge = max(target_col-max_i,target_row-max_j)
                    min_values,max_values,size,mod_count = mark_visited(min_values, max_values, size, mod_count, target_col-cells_past_edge, target_row-cells_past_edge)
            
            if cell_col != min_i:
                target_col = cell_col -radius
                target_row = cell_row
                if target_col >= min_i:
                    min_values,max_values,size,mod_count = mark_visited(min_values, max_values, size, mod_count, target_col, target_row)
                else:
                    cells_past_edge = min_i - target_col
                    min_values,max_values,size,mod_count = mark_visited(min_values, max_values, size, mod_count,target_col+cells_past_edge,target_row)
                    
            if cell_col != max_i:
                target_col = cell_col +radius
                target_row = cell_row
                if target_col <= max_i:
                    min_values,max_values,size,mod_count = mark_visited(min_values, max_values, size, mod_count, target_col, target_row)
                else:
                    cells_past_edge = target_col - max_i
                    min_values,max_values,size,mod_count = mark_visited(min_values, max_values, size, mod_count,target_col-cells_past_edge,target_row)
            
            if cell_col != min_i and cell_row !=min_j:
                target_col = cell_col - radius
                target_row = cell_row -radius
                if target_col >= min_i and target_row >= min_j:
                    min_values,max_values,size,mod_count = mark_visited(min_values, max_values, size, mod_count, target_col, target_row)
                else:
                    cells_past_edge = max(min_i-target_col,min_j-target_row)
                    min_values,max_values,size,mod_count = mark_visited(min_values, max_values, size, mod_count, target_col+cells_past_edge, target_row+cells_past_edge)
                    
            if cell_row != min_j:
                target_col = cell_col
                target_row = cell_row - radius
                if target_row >= min_j:
                    min_values,max_values,size,mod_count = mark_visited(min_values, max_values, size, mod_count,target_col,target_row)
                else:
                    cells_past_edge = min_j -target_row
                    min_values,max_values,size,mod_count = mark_visited(min_values, max_values, size, mod_count,target_col,target_row+cells_past_edge)
            
            if cell_col != max_i and cell_row != min_j:
                target_col = cell_col+radius
                target_row = cell_row-radius
                
                if target_col <=max_i and target_row >= min_j:
                    min_values,max_values,size,mod_count = mark_visited(min_values, max_values, size, mod_count, target_col,target_row)
                else:
                    cells_past_edge = max(target_col-max_i,min_j-target_row)
                    min_values,max_values,size,mod_count = mark_visited(min_values, max_values, size, mod_count,target_col-cells_past_edge,target_row+cells_past_edge)
    
    
    return min_values,max_values,size,mod_count

def mark_visited (min_values,max_values,size,mod,col,row):
    
    if min_values.size > col:

        if min_values[col] == -1:
                min_values[col] = row
                max_values[col] = row
                size = size +1
                mod = mod +1
        
        elif min_values[col] > row:
            size = size + min_values[col]-row
            min_values[col] = row
            mod = mod +1
        
        elif max_values[col] < row:
            size = size + row - max_values[col]
            max_values[col] = row
            mod = mod +1
            
    return min_values,max_values,size,mod

def constrained_time_warp(ts1,ts2,min_values,max_values,size,mod_count):
    cost_matrix_cell_values = np.zeros(size)
    cost_matrix_col_offset = np.zeros(min_values.size)
    current_off_set = 0
    for i in range(0,min_values.size):
        cost_matrix_col_offset[i] = current_off_set
        current_off_set = current_off_set + max_values[i]-min_values[i]+1

        
    maxI = ts1.size -1
    maxj = ts2.size -1
    has_next = False
    if size > 0: has_next = True
    
    i = j = 0
    
    current_i = i
    current_j = j
    expected_mod = mod_count

    while has_next:
        if expected_mod != mod_count:
            #throw Exception
            return
        elif has_next == False:
            #throw Exception
            return
        else:
            current_i = i
            current_j = j
            j += 1
            if j > max_values[current_i]:
                i += 1
                if i <= min_values.size-1:                    
                    j = min_values[i]
                else:
                    has_next = False
        
        if current_i == 0 and current_j == 0:
            distance = calc_distance.ecludian_distance(ts1[0], ts2[0])               
            cost_matrix_cell_values = put_val(current_i,current_j,min_values,max_values,cost_matrix_cell_values,cost_matrix_col_offset,distance)
        
        elif current_i ==0:
            val = get_val(current_i,current_j-1,min_values,max_values,cost_matrix_cell_values,cost_matrix_col_offset)   
            distance = calc_distance.ecludian_distance(ts1[0], ts2[current_j])
            distance += val
            cost_matrix_cell_values = put_val(current_i,current_j,min_values,max_values,cost_matrix_cell_values,cost_matrix_col_offset,distance)
            
        elif current_j ==0:
            val = get_val(current_i-1,current_j,min_values,max_values,cost_matrix_cell_values,cost_matrix_col_offset)   
            distance = calc_distance.ecludian_distance(ts1[current_i], ts2[0])
            distance += val
            cost_matrix_cell_values = put_val(current_i,current_j,min_values,max_values,cost_matrix_cell_values,cost_matrix_col_offset,distance)

        else:
            val1 = get_val(current_i-1,current_j,min_values,max_values,cost_matrix_cell_values,cost_matrix_col_offset)
            val2 = get_val(current_i-1,current_j-1,min_values,max_values,cost_matrix_cell_values,cost_matrix_col_offset)
            val3 = get_val(current_i,current_j-1,min_values,max_values,cost_matrix_cell_values,cost_matrix_col_offset)
            global_min_cost = min(val1,min(val2,val3)) 
            distance = calc_distance.ecludian_distance(ts1[current_i], ts2[current_j])
            cost_matrix_cell_values = put_val(current_i,current_j,min_values,max_values,cost_matrix_cell_values,cost_matrix_col_offset,distance+global_min_cost)

            
    minimum_cost = get_val(maxI, maxj, min_values, max_values, cost_matrix_cell_values, cost_matrix_col_offset)
    

    minimum_cost_path = np.empty(maxI+maxj-1, dtype='int8, int8')
            
    minimum_cost_path[:] = -1
    i,j = maxI,maxj
    minimum_cost_index = minimum_cost_path.size -1
    minimum_cost_path[minimum_cost_index] = (i,j)
    
    while i >0 or j >0:
        diag_cost = Decimal('Infinity')
        left_cost = Decimal('Infinity')
        down_cost = Decimal('Infinity')
        
        if (i > 0) and (j > 0): 
            diag_cost = get_val(i-1, j-1, min_values, max_values, cost_matrix_cell_values, cost_matrix_col_offset)
        if i > 0: 
            left_cost = get_val(i-1, j, min_values, max_values, cost_matrix_cell_values, cost_matrix_col_offset)
        if j > 0:             
            down_cost = get_val(i, j-1, min_values, max_values, cost_matrix_cell_values, cost_matrix_col_offset)
        
        if (diag_cost <= left_cost and diag_cost <= down_cost):
            i = i-1
            j = j-1
        elif (left_cost < diag_cost and left_cost < down_cost):
            i = i-1
        elif (down_cost<diag_cost and down_cost<left_cost):
            j = j -1
        elif i <= j:
            j = j -1
        else:
            i = i-1
        minimum_cost_index = minimum_cost_index -1
        minimum_cost_path[minimum_cost_index] = (i,j)
        
        
    temp = np.arange(minimum_cost_index)
    minimum_cost_path = np.delete(minimum_cost_path,temp)
    return minimum_cost,minimum_cost_path

    
def get_val(col,row,min_values,max_values,cost_matrix_cell_values,cost_matrix_col_offset):    
    if row < min_values[col] or row > max_values[col]:
        return Infinity
    else:
        return cost_matrix_cell_values[cost_matrix_col_offset[col]+row-min_values[col]]
    
    
def put_val(col,row,min_values,max_values,cost_matrix_cell_values,cost_matrix_col_offset,distance):
    if row < min_values[col] or row > max_values[col]:
        #throw exceptoin
        return cost_matrix_cell_values
    else:                
        cost_matrix_cell_values[cost_matrix_col_offset[col]+row-min_values[col]] = distance
    
    return cost_matrix_cell_values
    
    
    
    
    