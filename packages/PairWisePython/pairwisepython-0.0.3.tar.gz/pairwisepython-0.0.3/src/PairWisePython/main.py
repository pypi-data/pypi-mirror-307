from itertools import combinations, permutations


def generate_pairs(parameters):
    pairs = []
    for param_values in parameters:
        pairs.extend(list(combinations(param_values, 2)))
    return pairs
