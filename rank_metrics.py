def mean_reciprocal_rank(rs):
    """Score is reciprocal of the rank of the first relevant item

    First element is "rank 1" so as to not result in infinity.  Relevance is
    binary (nonzero is relevant).

    Example from http://en.wikipedia.org/wiki/Mean_reciprocal_rank
    >>> rs = [[0, 0, 1], [0, 1, 0], [1, 0, 0]]
    >>> mean_reciprocal_rank(rs)
    0.6111111111111112

    Args:
        rs: List of relevance scores in rank order (first element is the first item)

    Returns:
        Mean reciprocal rank
    """
    return np.mean([1. / (np.asfarray(r).nonzero()[0] + 1) for r in rs])


def rank_precision_k():
    pass