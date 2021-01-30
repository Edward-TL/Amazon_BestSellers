import pandas as pd

def count_if(array, value):
    count = 0
    for element in array:
        if element == value:
            count += 1
    return count

def array_count(elements_to_count, original_array):
    count_array = [None] * len(elements_to_count)
    c = 0

    for value in range(len(elements_to_count)):
        count_array[c] = original_array.count(elements_to_count[value])
        c += 1
        
    return count_array

def reverse(array):
    reversed_array = [None]*len(array)
    n = 0
    for data in reversed(array):
        reversed_array[n] = data
        n += 1

    return reversed_array

def rank_set_list(df, rank, info, set_list=True, array=True):
    ranking = df[df['Rank'] == rank]
    raw_info_in_rank = ranking[info].to_list()

    if set_list == True:
        set_info = list(set(raw_info_in_rank))
        none_cases = count_if(set_info, None)
        if none_cases > 0:
            set_info.remove(None)

        if array == True:
            return set_info, raw_info_in_rank

        else: return set_info
    
    else: return raw_info_in_rank

def rank_info(df, rank, column_info, info_name='Albums'):
    set_info, raw_info_in_rank = rank_set_list(df, rank, column_info)
    info_count = array_count(elements_to_count=set_info, original_array=raw_info_in_rank)
    info = {info_name: set_info,
            'Counts' : info_count}
    df_info = pd.DataFrame(info)
    df_info = df_info.sort_values(by=['Counts'])

    return df_info