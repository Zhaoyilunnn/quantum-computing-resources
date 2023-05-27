import random


def select_n_integers(n, range_start, range_end):
    # Create a list of integers in the given range
    integer_range = list(range(range_start, range_end))

    # Use random.sample() to select n unique integers from the range
    selected_integers = random.sample(integer_range, n)

    return selected_integers

def split_list(lst, num_groups):
    quotient = len(lst) // num_groups  # Number of elements per group 
    remainder = len(lst) % num_groups  # Number of elements in last group

    result = []
    start_index = 0
    for i in range(num_groups):
        if i < remainder: 
            end_index = start_index + quotient + 1
        else:
            end_index = start_index + quotient
        result.append(lst[start_index:end_index])
        start_index = end_index

    return result
