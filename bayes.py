import math
from functools import reduce
from operator import mul


class NoDataError(Exception):
    pass


LARGE_NUM = 10.0**20


def base_probability(pos_count, neg_count, pos_all, neg_all):
    pos_freq = pos_count / pos_all
    neg_freq = neg_count / neg_all
    return pos_freq / (pos_freq + neg_freq)


def bayesian_probability(pos_count, neg_count, pos_all, neg_all, prior):
    base_prob = base_probability(pos_count, neg_count, pos_all, neg_all)
    num_samples = pos_count + neg_count
    return (prior + num_samples*base_prob) / (1 + num_samples)


def inverse_chi_square(value, degree_of_freedom):
    m = value / 2
    a = math.exp(-m)
    result = 0
    for i in range(degree_of_freedom//2):
        result += a
        a *= m / (i+1)
    # Floating point arithmetic are not precise.
    # We need to cap the result due to this imprecision.
    return min(result, 1.0)


def fisher_method(probabilities):
    if not len(probabilities):
        raise NoDataError
    prob = reduce(mul, probabilities)
    log_prob = math.log(prob) if prob > 0 else -LARGE_NUM
    return inverse_chi_square(-2*log_prob, 2*len(probabilities))


def calculate_score(data, pos_all, neg_all, prior):
    """
    Calculate a score for data.
    Value of data should be a list of (positive_count, negative_count).
    """
    pos_probs = [
        bayesian_probability(pos_count, neg_count, pos_all, neg_all, prior)
        for pos_count, neg_count in data
        if pos_count + neg_count
    ]
    neg_probs = [1-p for p in pos_probs]
    pos_score = 1 - fisher_method(neg_probs)
    neg_score = 1 - fisher_method(pos_probs)
    return (pos_score + (1-neg_score)) / 2


__all__ = ['NoDataError', 'calculate_score']
