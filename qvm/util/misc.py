import random

def select_n_integers(n, range_start, range_end):
    # Create a list of integers in the given range
    integer_range = list(range(range_start, range_end))

    # Use random.sample() to select n unique integers from the range
    selected_integers = random.sample(integer_range, n)

    return selected_integers

