from itertools import combinations, permutations


def generate_pairs(parameters):
    pairs = []
    for param_values in parameters.values():
        pairs.extend(list(combinations(param_values, 2)))
    return pairs


def pairwise_testing(parameters):
    all_params = list(parameters.keys())
    pairs = generate_pairs(parameters)

    test_cases = []
    for pair in pairs:
        test_case = {}
        for param in all_params:
            test_case[param] = None

        first_param = next((k for k, v in parameters.items() if pair[0] in v), None)
        second_param = next((k for k, v in parameters.items() if pair[1] in v), None)

        test_case[first_param] = pair[0]
        test_case[second_param] = pair[1]

        test_cases.append(test_case)

    return test_cases
